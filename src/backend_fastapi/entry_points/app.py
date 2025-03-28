"""Entry point for _run_app()."""

import click
from loguru import logger
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend_fastapi.endpoints import auth_router, experiences_router, users_router

@click.command()
@click.option("--host")
@click.option("--port")
def run_app(host: str, port: str) -> str:
    """Entry point to say hello.

    Args:
        host: Host.
        port: Port.

    Returns:
        Greet.
    """
    return _run_app(host, port)


def _run_app(host: str, port: str) -> str:
    """Say hello to user.

    Args:
        host: Host.
        port: Port.

    Returns:
        Greet.
    """
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

    uvicorn.run(app, host=host, port=int(port))

