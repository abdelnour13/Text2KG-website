"""
API routes for /graphs.

All routes follow the pattern:
  route → service → db queries
"""

from fastapi import APIRouter, Depends, Response, Query
from neo4j import Session
from typing import Optional
from src.config import Settings, get_settings
from src.db.neo4j import get_session
from src.schemas.graph import GraphSummary, GraphDetail, VisualisationResponse
from src.services.graph_service import GraphService
from src.utils.visualisation import (
    build_taxonomy_vis,
    build_expertises_vis,
    build_expertise_detail_vis,
    build_summary_vis
)

router = APIRouter(prefix="/graphs", tags=["graphs"])

_service = GraphService()


def _vis_url(settings: Settings, filename: str) -> str:
    """Build the public URL for a generated visualisation file."""
    return f"{settings.app_public_base_url.rstrip('/')}/public/visualizations/{filename}"


# ── 1. List all graphs ────────────────────────────────────────────────────────

@router.get(
    "",
    response_model=list[GraphSummary],
    summary="List all expertise maps",
)
def list_graphs(
    session: Session = Depends(get_session),
) -> list[GraphSummary]:
    """Return a summary row for every ExpertiseMap stored in Neo4j."""
    return _service.list_graphs(session)


# ── 2. Get graph by ID ────────────────────────────────────────────────────────

@router.get(
    "/{graph_id}",
    response_model=GraphDetail,
    summary="Get full detail for an expertise map",
    responses={404: {"description": "Graph not found"}},
)
def get_graph(
    graph_id: str,
    session: Session = Depends(get_session),
) -> GraphDetail:
    """Return domains, subdomains, expertises and entity count for *graph_id*."""
    return _service.get_graph(session, graph_id)


# ── 3. Download graph as JSON ─────────────────────────────────────────────────

@router.get(
    "/{graph_id}/download",
    summary="Download the subgraph as JSON via APOC streaming",
    responses={
        200: {"content": {"application/json": {}}},
        404: {"description": "Graph not found"},
        500: {"description": "Export error"},
    },
)
def download_graph(
    graph_id: str,
    session: Session = Depends(get_session),
) -> Response:
    """
    Export the entire subgraph for *graph_id* using APOC streaming.

    Nothing is written to disk — the JSON is streamed and returned directly
    with the appropriate download headers.
    """
    json_data = _service.download_graph(session, graph_id)
    return Response(
        content=json_data,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="graph_{graph_id}.json"'
        },
    )


# ── 4. Visualise taxonomy ─────────────────────────────────────────────────────

@router.post(
    "/{graph_id}/vis/taxonomy",
    response_model=VisualisationResponse,
    summary="Generate Domain → SubDomain taxonomy visualisation",
    responses={404: {"description": "Graph not found"}},
)
def vis_taxonomy(
    graph_id: str,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> VisualisationResponse:
    """Build and persist an interactive HTML graph of the taxonomy."""
    data = _service.get_taxonomy_data(session, graph_id)
    filename = build_taxonomy_vis(data)
    return VisualisationResponse(url=_vis_url(settings, filename), filename=filename)


# ── 5. Visualise all expertises ───────────────────────────────────────────────

@router.post(
    "/{graph_id}/vis/expertises",
    response_model=VisualisationResponse,
    summary="Generate Expertise ↔ SubDomain ↔ Domain visualisation",
    responses={404: {"description": "Graph not found"}},
)
def vis_expertises(
    graph_id: str,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
    domains : Optional[list[str]] = Query(default=None),
    subdomains : Optional[list[str]] = Query(default=None),
    labs : Optional[list[str]] = Query(default=None),
) -> VisualisationResponse:
    """Build and persist an interactive HTML graph of all expertises."""
    data = _service.get_expertises_data(session, graph_id, subdomains, domains, labs)
    filename = build_expertises_vis(data)
    return VisualisationResponse(url=_vis_url(settings, filename), filename=filename)


# ── 6. Visualise a single expertise ──────────────────────────────────────────

@router.post(
    "/{graph_id}/vis/expertises/{expertise_id}",
    response_model=VisualisationResponse,
    summary="Generate detailed visualisation for a single Expertise",
    responses={
        404: {"description": "Graph or Expertise not found"},
    },
)
def vis_expertise_detail(
    graph_id: str,
    expertise_id: str,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> VisualisationResponse:
    """
    Build and persist an interactive HTML graph showing:
    Expertise ↔ Entity, Expertise ↔ SubDomain, SubDomain ↔ Domain,
    Entity ↔ SubDomain.
    """
    data = _service.get_expertise_detail_data(session, graph_id, expertise_id)
    filename = build_expertise_detail_vis(data)
    return VisualisationResponse(url=_vis_url(settings, filename), filename=filename)

# ── 7. Summary statistics visualisation ──────────────────────────────────────

@router.post(
    "/{graph_id}/vis/summary",
    response_model=VisualisationResponse,
    summary="Generate summary statistics bar charts",
    responses={404: {"description": "Graph not found"}},
)
def vis_summary(
    graph_id: str,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> VisualisationResponse:
    """
    Build and persist a self-contained HTML page with 10 bar/stacked-bar charts:
      - Articles by Lab, Domain, SubDomain
      - Articles by Domain & Lab (stacked), by SubDomain & Lab (stacked)
      - Expertises by Lab, Domain, SubDomain
      - Expertises by Domain & Lab (stacked), by SubDomain & Lab (stacked)
    """
    data = _service.get_summary_data(session, graph_id)
    filename = build_summary_vis(data)
    return VisualisationResponse(url=_vis_url(settings, filename), filename=filename)
