# libraries
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    secret_key: str

    class Config:
        env_file = os.path.join(os.getcwd(), '.env')


settings = Settings()
