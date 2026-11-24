"""Pydantic schemas for API request / response validation."""

from pydantic import BaseModel, Field


# ── Graph list ────────────────────────────────────────────────────────────────

class GraphSummary(BaseModel):
    """Lightweight representation returned by GET /graphs."""

    id: str
    description: str
    number_of_expertises: int
    labs: list[str]
    domains : list[str]
    subdomains: list[str]


# ── Graph detail ──────────────────────────────────────────────────────────────

class DomainSchema(BaseModel):
    id: str
    name: str


class SubDomainSchema(BaseModel):
    id: str
    name: str
    # domain: str


class ExpertiseSchema(BaseModel):
    id: str
    personalized_pagerank_name: str
    llm_label: str
    size: int
    domains : list[str] = Field(default_factory=list)
    labs : list[str] = Field(default_factory=list)
    subdomains: list[str] = Field(default_factory=list)


class EntitySchema(BaseModel):
    id: str
    name: str
    generality_score: float | None = None
    relevancy_score: float | None = None
    pagerank: float | None = None
    specifity_weighted_pagerank: float | None = None
    degree: int | None = None


class GraphDetail(BaseModel):
    """Full representation returned by GET /graphs/{id}."""

    id: str
    description: str
    domains: list[str]
    labs : list[str]
    subdomains: list[str]
    expertises: list[ExpertiseSchema]
    entity_count: int


# ── Visualisation ─────────────────────────────────────────────────────────────

class VisualisationResponse(BaseModel):
    """URL pointing to the generated HTML visualisation."""

    url: str
    filename: str


# ── Generic error (matches FastAPI HTTPException detail shape) ────────────────

class ErrorDetail(BaseModel):
    detail: str
