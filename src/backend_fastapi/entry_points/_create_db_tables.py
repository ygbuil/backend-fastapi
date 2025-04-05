"""Entry point for _run_app()."""

import click
from loguru import logger

from backend_fastapi.data import Base
from backend_fastapi.data.database import engine


@click.command()
def create_db_tables() -> None:
    """Create database.

    Returns:
        None.
    """
    _create_db_tables()


def _create_db_tables() -> None:
    """Create database.

    Returns:
        None.
    """
    logger.info("Creating database tables.")
    Base.metadata.create_all(bind=engine)  # type: ignore
