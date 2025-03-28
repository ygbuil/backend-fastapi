"""App entry point."""

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
