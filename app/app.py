# libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# local libraries
from app.endpoints.auth import auth_router
from app.endpoints.users import users_router
from app.endpoints.experiences import experiences_router


app = FastAPI()
routers = [auth_router, users_router, experiences_router]

for router in routers:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_credentials=True,
    allow_methods=['*'], allow_headers=['*'],
)
