"""
Expertise Map API — entry point.

Startup / shutdown lifecycle:
  - connects the Neo4j driver on startup
  - closes it cleanly on shutdown

Static files:
  - /public  →  app/public/  (visualisation HTML files)
"""

import json
from contextlib import asynccontextmanager
from http import HTTPStatus
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.graphs import router
from src.config import get_settings
from src.db.neo4j import init_driver, close_driver
from definitions import DIR

PUBLIC_DIR = DIR / "public"
APP_DIR = DIR / "app"
VIS_DIR = PUBLIC_DIR / "visualizations"
PUBLIC_DIR.mkdir(parents=True, exist_ok=True)


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("LIFESPAN START", flush=True)
    settings = get_settings()
    print("GOT SETTINGS", flush=True)

    await init_driver(settings)

    yield

    close_driver()


# ── Application ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="Expertise Map API",
    description=(
        "Backend service for exploring and visualising expertise maps "
        "stored in Neo4j."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://0.0.0.0:5173",
    "http://0.0.0.0:8000",
    "http://51.210.13.71:8000",
    "http://51.210.13.71:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Static files ──────────────────────────────────────────────────────────────

app.mount("/public", StaticFiles(directory=str(PUBLIC_DIR)), name="public")

# ── Routers ───────────────────────────────────────────────────────────────────

app.include_router(router)


# ── Global error handler ──────────────────────────────────────────────────────

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": f"Unexpected server error: {exc}"},
    )

# ── File download endpoint ────────────────────────────────────────────────────

@app.get("/download/{filename}")
def download_file(filename: str):

    file_path = VIS_DIR / filename

    if not file_path.exists():
        print(file_path)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"File {filename} doesn't exist.")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='text/html',
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/health", tags=["meta"])
def health() -> dict:
    """Simple liveness probe."""
    return {"status": "ok"}