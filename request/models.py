"""
    Request Models module
"""
from pydantic import BaseModel, constr, EmailStr


class Student(BaseModel):
    identification: str
    name: constr(regex=r'^[a-zA-Z\s]+$')
    lastname: constr(regex=r'^[a-zA-Z\s]+$')
    age: int
    email: EmailStr
    affinity: int


class IdStudent(BaseModel):
    identification: str


class UpdateRequest(BaseModel):
    request_id: int
    is_aprove: str


class Grimoire(BaseModel):
    name: str
