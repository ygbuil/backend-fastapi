"""Entry point for _run_app()."""

import click
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend_fastapi.endpoints import auth_router, experiences_router, users_router

app = FastAPI()
routers = [auth_router, users_router, experiences_router]

for router in routers:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@click.command()
@click.option("--host")
@click.option("--port")
def run_app(host: str, port: str) -> None:
    """Entry point to run the app.

    Args:
        host: Host.
        port: Port.

    Returns:
        None.
    """
    _run_app(host, port)


def _run_app(host: str, port: str) -> None:
    """Run the app.

    Args:
        host: Host.
        port: Port.

    Returns:
        None.
    """
    uvicorn.run(app, host=host, port=int(port))
