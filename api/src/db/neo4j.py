"""Neo4j driver lifecycle and FastAPI dependency."""

import asyncio
from typing import Generator

from fastapi import Depends
from neo4j import GraphDatabase, Driver, Session

from src.config import Settings, get_settings


_driver: Driver | None = None


async def init_driver(settings):

    global _driver

    for attempt in range(10):
        try:
            print(f"Attempt {attempt}", flush=True)

            _driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password),
            )

            _driver.verify_connectivity()

            print("Connected to database")
            return

        except Exception as e:
            print(f"Neo4j connection failed: {repr(e)}")
            await asyncio.sleep(5)

    raise RuntimeError("Could not connect to Neo4j")


def close_driver() -> None:
    """Close the module-level driver (called at shutdown)."""
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


def get_driver() -> Driver:
    """Return the live driver; raises if not initialised."""
    if _driver is None:
        raise RuntimeError("Neo4j driver has not been initialised.")
    return _driver


def get_session(
    driver: Driver = Depends(get_driver),
    settings: Settings = Depends(get_settings),
) -> Generator[Session, None, None]:
    """FastAPI dependency that yields a Neo4j session."""
    with driver.session(database=settings.neo4j_database) as session:
        yield session
