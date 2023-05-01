import os

from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from fastapi.security import OAuth2PasswordBearer

from data.server import create_engine_data

db = create_engine_data()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def create_app():
    """
        create an FastAPI instance

    Returns:
        FastAPI, APIRoute: fastapi instance and route
    """
    load_dotenv()
    app = FastAPI()
    api = APIRouter(prefix='/api/v1')

    app.config = {
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_DATABASE_URI')
    }

    return app, api
