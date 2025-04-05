"""Entry points for initial_repository_template."""

import click

from backend_fastapi import entry_points


def _main() -> None:
    """Gathers all entry points of the program."""

    @click.group(chain=True)
    def entry_point() -> None:
        """Entry point."""

    for command in (entry_points.run_app, entry_points.create_db_tables):
        entry_point.add_command(command)

    entry_point()
