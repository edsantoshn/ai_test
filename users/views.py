"""
    User Module Views
"""
import os
from datetime import datetime, timedelta
from typing import Annotated, Union


from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext


from data.query import get_user_by_username
from .models import *


load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        os.getenv('SECRET_KEY'),
        algorithm=os.getenv('ALGORITHM'))
    return encoded_jwt


async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """verify if the username exist or not, if it exist create 

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends): to verify by bearer

    Returns:
        dict or json: return an json element or dict with status as a obligatory
        field which is a bool type if it exist the value is True otherwise False.
    """
    user = get_user_by_username(form_data.username)
    print(user, form_data)

    if not user:
        return {"status":False, "message":"Please verify your username"}

    if not pwd_context.verify(form_data.password, user.password):
        return {"message":"Wrong Password!", "status":False}

    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "status":True}
