"""
    User Module Views
"""
from typing import Annotated


from dotenv import load_dotenv
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from jose import jwt
from passlib.context import CryptContext


from data.query import (
    make_student, make_request,
    update_student, get_student,
    delete_student, update_request,
    list_students, get_grimoire,
    list_magic_affinity)
from users.models import User
from util.auth import get_current_user
from util.validators import validate_letters_only, validate_letters_and_number
from .models import *


load_dotenv()


def make_student_request(data:Student) -> dict:
    """create a student request

    Args:
        data (Student): model name and lastname must cointain only letters,
        identification must have letters and numbers.
        The affinity its an integer if you need to assign it get the list of them.

    Returns:
        dict: statusCode 400 or 201 and body (is a message)
    """
    if not validate_letters_and_number(data.identification):
        return {"statusCode":400, "body":"The identification must contain letters and numers!"}

    if not validate_letters_only(data.name):
        return {"statusCode":400, "body":"The name must be only letters!"}

    if not validate_letters_only(data.lastname):
        return {"statusCode":400, "body":"The lastname must be only letters!"}

    is_inserted = make_student(jsonable_encoder(data))

    if not is_inserted['status']:
        return {"statusCode":204, "body":is_inserted["message"]}

    is_requested = make_request(str(data.identification))

    if not is_requested['status']:
        return {"statusCode":204, "body":is_requested["message"]}

    return {"statusCode":201, "body":"Your request was created successfully!"}


def update_student_request(data:Student) -> dict:
    """update a student request

    Args:
        data (Student): model name and lastname must cointain only letters,
        identification must have letters and numbers, identification is not mutable.

    Returns:
        dict: statusCode 400 or 201 and body (is a message)
    """
    if not validate_letters_and_number(str(data.identification)):
        return {"statusCode":400, "body":"The identification must contain letters and numers!"}

    if not validate_letters_only(data.name):
        return {"statusCode":400, "body":"The name must be only letters!"}

    if not validate_letters_only(data.lastname):
        return {"statusCode":400, "body":"The lastname must be only letters!"}

    is_inserted = update_student(jsonable_encoder(data))

    if not is_inserted['status']:
        return {"statusCode":204, "body":"Your student was not updated successfully!"}

    return {"statusCode":201, "body":"Your request was updated successfully!"}


def delete_request(data: IdStudent) -> dict:
    """Delete a student a request data

    Args:
        data (IdStudent): _description_

    Returns:
        dict: statusCode 400 or 204 and body (is a message)
    """
    student = get_student(data.identification)
    if not student:
        return {"statusCode":400, "body":"The student doesn't exist!"}

    is_delete = delete_student(data.identification)
    if is_delete:
        return {"statusCode":204, "body":"Your student was deleted successfully!"}

    return is_delete


def update_request_status(data:UpdateRequest) -> dict:
    """update the status request 1 if it aprove 2 if it denied

    Args:
        data (UpdateRequest): unique request id a is_aprove field

    Returns:
        dict: status code and message
    """
    type_process = 'aproved' if data.is_aprove == '1' else 'denied'

    is_update = update_request(jsonable_encoder(data))
    if is_update['status']:
        return {"statusCode":204, "body": f"The request was {type_process} successfully!"}
    return is_update


def get_students_list(cu_user: Annotated[User, Depends(get_current_user)]) -> dict:
    """get the list of students

    Args:
        cu_user (Annotated[User, Depends): _description_
    """
    students = list_students()
    data = list(map(lambda x: {
        "id": x.identification,
        "name": x.name,
        "lastname": x.lastname,
        "status": x.requests[0].is_aprove}, students))
    return {"statusCode":200, "data":data, "body":"Data was get successfuly!"}


def query_grimoires_list(cu_user: Annotated[User, Depends(get_current_user)]) -> dict:
    """Get a grimoire name a return the list of students match with

    Args:
        cu_user (Annotated[User, Depends): to verify the current user
    """
    grimoires = get_grimoire()
    if not grimoires['status']:
        return {"statusCode":204,  "body":f"there isn't data to {data.name}!"}

    data = list()
    for row in grimoires['data']:
        grimori, count = row
        data.append({
            "id": grimori.id,
            "name": grimori.name,
            "count": count
        })
    return {"statusCode":200, "data":data, "body":"Data was get successfuly!"}


def list_affinities() -> dict:
    """return a list of affinities

    Returns:
        dict: statusCode, body and data
    """
    data = list_magic_affinity()
    return {"statusCode":200, "data":data, "body":"Data was get successfuly!"}
