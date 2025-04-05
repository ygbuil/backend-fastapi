"""Entry point for _run_app()."""

import click

from backend_fastapi.data import Base
from backend_fastapi.data.database import engine


@click.command()
def create_database() -> None:
    """Create database.

    Returns:
        None.
    """
    _create_database()


def _create_database() -> None:
    """Create database.

    Returns:
        None.
    """
    Base.metadata.create_all(bind=engine)  # type: ignore
