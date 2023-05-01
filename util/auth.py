"""
    Authentication module
"""
import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from users.models import User
from data.query import get_user_by_username
from .database import oauth2_scheme
from .models import TokenData


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            os.getenv('SECRET_KEY'),
            algorithms=[os.getenv('ALGORITHM')])

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = TokenData(username=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    user = User(**user.__dict__)
    return user
