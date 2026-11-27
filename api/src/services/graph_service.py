"""
Graph service.

Sits between the API routes and the DB query layer.
Responsible for:
  - orchestrating multi-query operations
  - mapping raw Neo4j dicts onto Pydantic schemas
  - raising appropriate HTTPExceptions
"""

from fastapi import HTTPException, status
from neo4j import Session

from src.db.queries import (
    fetch_all_graphs,
    fetch_graph_by_id,
    graph_exists,
    stream_graph_json,
    fetch_taxonomy,
    fetch_expertises_graph,
    fetch_expertise_detail,
    fetch_summary_stats
)

from src.schemas.graph import (
    GraphSummary,
    GraphDetail,
)


class GraphService:
    """Stateless service — receives a Neo4j session per call."""

    # ── Listings ──────────────────────────────────────────────────────────────

    def list_graphs(self, session: Session) -> list[GraphSummary]:
        """Return a summary for every ExpertiseMap in the database."""
        try:
            rows = fetch_all_graphs(session)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while listing graphs: {exc}",
            ) from exc

        return [
            GraphSummary(
                id=row["id"],
                name=row['name'],
                description=row.get("description", "No description available."),
                number_of_expertises=row.get("number_of_expertises", 0),
                domains=row.get("domains", []),
                labs=row.get("labs", []),
                subdomains=row.get("subdomains", []),
            )
            for row in rows
        ]

    # ── Single graph ──────────────────────────────────────────────────────────

    def get_graph(self, session: Session, graph_id: str) -> GraphDetail:
        """Return full detail for one ExpertiseMap or raise 404."""
        try:
            row = fetch_graph_by_id(session, graph_id)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching graph '{graph_id}': {exc}",
            ) from exc

        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Graph '{graph_id}' not found.",
            )

        # domains = [DomainSchema(id=d["id"], name=d.get("name", "")) for d in row["domains"]]
        # subdomains = [
        #     SubDomainSchema(
        #         id=sd["id"],
        #         name=sd.get("name", ""),
        #         domain=sd.get("domain", ""),
        #     )
        #     for sd in row["subdomains"]
        # ]
        # expertises = [
        #     ExpertiseSchema(
        #         id=ex["id"],
        #         label=ex.get("label", ""),
        #         size=ex.get("size", 0),
        #         subdomains=ex.get("subdomains", []),
        #     )
        #     for ex in row["expertises"]
        # ]

        return GraphDetail(**row)

    # ── Download ──────────────────────────────────────────────────────────────

    def download_graph(self, session: Session, graph_id: str) -> str:
        """
        Stream-export the subgraph via APOC and return raw JSON string.

        Raises 404 if the graph does not exist.
        Raises 500 on APOC / driver errors.
        """
        self._assert_exists(session, graph_id)

        try:
            json_data = stream_graph_json(session, graph_id)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Export failed for graph '{graph_id}': {exc}",
            ) from exc

        if not json_data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"APOC returned empty data for graph '{graph_id}'.",
            )

        return json_data

    # ── Visualisation data fetchers ───────────────────────────────────────────

    def get_taxonomy_data(self, session: Session, graph_id: str) -> list[dict]:
        """Return taxonomy rows for the given graph or raise 404."""
        self._assert_exists(session, graph_id)
        try:
            return fetch_taxonomy(session, graph_id)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch taxonomy for '{graph_id}': {exc}",
            ) from exc

    def get_expertises_data(self, 
        session: Session, 
        graph_id: str, 
        subdomains: list[str] | None = None,
        domains: list[str] | None = None,
        labs : list[str] | None = None
    ) -> dict:
        """Return expertises graph data or raise 404."""
        self._assert_exists(session, graph_id)

        try:
            return fetch_expertises_graph(session, graph_id, subdomains, domains, labs)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch expertises for '{graph_id}': {exc}",
            ) from exc

    def get_expertise_detail_data(
        self, session: Session, graph_id: str, expertise_id: str
    ) -> dict:
        """Return single expertise graph data or raise 404."""
        self._assert_exists(session, graph_id)
        try:
            data = fetch_expertise_detail(session, graph_id, expertise_id)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch expertise '{expertise_id}': {exc}",
            ) from exc

        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Expertise '{expertise_id}' not found in graph '{graph_id}'.",
            )
        return data

    # ── Private helpers ───────────────────────────────────────────────────────

    def _assert_exists(self, session: Session, graph_id: str) -> None:
        """Raise 404 if the ExpertiseMap does not exist."""
        try:
            exists = graph_exists(session, graph_id)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while checking graph '{graph_id}': {exc}",
            ) from exc
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Graph '{graph_id}' not found.",
            )
        
    def get_summary_data(self, session: Session, graph_id: str) -> dict:
        """Return all summary statistics for the given graph or raise 404."""
        self._assert_exists(session, graph_id)
        try:
            return fetch_summary_stats(session, graph_id)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch summary stats for '{graph_id}': {exc}",
            ) from exc
