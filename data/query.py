import random
from typing import Dict, Any, Text


from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy import func as f
from sqlalchemy.sql import func
from sqlalchemy.orm import Session


from .models import MagicAffinity, Student, User, Request, Grimoire
from .server import create_engine_data


load_dotenv()
engine = create_engine_data()


def get_user_by_username(username:Text):
    """find a user object if find return it otherwise return an false as status

    Args:
        username (Text): unique username
    """
    try:
        session = Session(engine)
        user = session.query(User).get(username)
        session.close()
        return user
    except Exception as exception:
        return {"message": f"There was an error at: {exception}", "status":None}


def get_student(identification:Text):
    """find a student object if find return it otherwise return an false as status

    Args:
        identification (Text): unique student id
    """
    try:
        session = Session(engine)
        student = session.query(Student).filter(Student.identification==identification).first()
        session.close()
        if len(student) > 0:
            return student
        else:
            return False
    except Exception as exception:
        return {"message": f"There was an error at: {exception}", "status":None}


def make_student(data:Dict[Any, Any])-> Dict[Any, Any]:
    """create or make a student request.

    Args:
        data (Dict[Any, Any]): identification, name, lastname, age, affinity

    Returns:
        Dict[Any, Any]: status, message
    """
    try:
        session = Session(engine)
        student = Student(
            identification=data['identification'],
            name=data['name'],
            lastname=data['lastname'],
            email=data['email'],
            age=data['age'],
            affinity=data["affinity"])
        session.add(student)
        session.commit()
        session.close()
        return {"message":"Request was registered successfully!", "status": True}
    except Exception as generic_error:
        return  {"message":f"There was an error trying to create a student: {generic_error}",
                 "status": None}


def update_student(data:Dict[Any, Any])-> Dict[Any, Any]:
    """update a student request.

    Args:
        data (Dict[Any, Any]): identification, name, lastname, age, affinity
        identification is primary key because of that couldn't be updated but
        its using to get the student data.

    Returns:
        Dict[Any, Any]: status, message
    """
    try:
        session = Session(engine)
        student = session.query(Student).get(data['identification'])
        if student:
            student.name = data['name']
            student.lastname = data['lastname']
            student.age = data['age']
            student.email = data['email']
            student.affinity = data['affinity']
            student.updated_at = func.now()
            session.commit()
        session.close()
        return {"message":"Request was updated successfully!", "status": True}
    except Exception as generic_error:
        return  {"message":f"There was an error trying to create a student: {generic_error}",
                 "status": None}


def delete_student(identification:Text):
    """Delete a student and request objects assosiated to it.

    Args:
        identification (Text): unique student id

    Returns:
        bool: True if successful or Dict otherwise none status y message
    """
    try:
        session = Session(engine)
        student = session.query(Student).filter(Student.identification==identification).first()
        request = session.query(Request).filter(Request.student==identification).first()
        session.delete(student)
        session.delete(request)
        session.commit()
        return True
    except Exception as exception:
        return {"message": f"There was an error at: {exception}", "status":None}


def list_students():
    """get the entire students list

    Returns:
        ditc: status and data
    """
    try:
        session = Session(engine)
        students = session.query(Student).all()
        return students
    except Exception as exception:
        return {"message": f"There was an error at: {exception}", "status":None}


def list_magic_affinity():
    """get the entire magic affinity list

    Returns:
        ditc: status and data
    """
    try:
        session = Session(engine)
        magic_affinities = session.query(MagicAffinity).all()
        return {"data":magic_affinities, "status":True}
    except Exception as exception:
        return {"message": f"There was an error at: {exception}", "status":None}


def list_grimoire():
    """get the entire grimoire list

    Returns:
        ditc: status and data
    """
    try:
        session = Session(engine)
        grimoire = session.query(Grimoire).all()
        return {"data":grimoire, "status":True}
    except Exception as exception:
        return {"message": f"There was an error at: {exception}", "status":None}



def make_request(identification:str)-> Dict[Any, Any]:
    """create or make a request.

    Args:
        identification (str): unique person id or dni

    Returns:
        Dict[Any, Any]: status, message
    """
    try:
        session = Session(engine)
        request = Request(
            student=identification,
            is_aprove='0')
        session.add(request)
        session.commit()
        session.close()
        return {"message":"Request was registered successfully!", "status": True}
    except Exception as generic_error:
        return  {"message":f"There was an error trying to make a request: {generic_error}",
                 "status": None}


def update_request(data:Dict[Any, Any])-> Dict[Any, Any]:
    """update a request.

    Args:
        data (Dict[Any, Any]): id, is_aprove.

    Returns:
        Dict[Any, Any]: status, message
    """
    try:
        session = Session(engine)
        request = session.query(Request).get(data['request_id'])
        if request:
            request.is_aprove = data['is_aprove']
            request.updated_at = func.now()
            

            if data['is_aprove'] == '1':
                grimoire = get_random_grimoire()
                student = session.query(Student).get(request.student)
                student.grimoire = grimoire.id
            session.commit()

        session.close()
        return {"message":"Request was updated successfully!", "status": True}
    except Exception as generic_error:
        return  {"message":f"There was an error trying to create a student: {generic_error}",
                 "status": None}


def get_grimoire():
    """Get a list of grimoires with the count of student.
    """
    try:
        session = Session(engine)
        data = session.query(Grimoire, f.count(Student.grimoire)).join(Student).group_by(Grimoire.id).all()
        return {"status":True, "data":data}
    except Exception as generic_error:
        return  {"message":f"There was an error trying to create a student: {generic_error}",
                 "status": None}


def get_random_grimoire():
    """get a random grimoire from the database

    Returns:
        "Grimoire": Grimoire object
    """
    try:
        session = Session(engine)
        total = session.query(func.count(Grimoire.id)).scalar()
        random_id = random.randint(1, total)
        grimoire = session.query(Grimoire).filter(Grimoire.id==random_id).first()
        return grimoire
    except Exception as generic_error:
        return  {"message":f"There was an error trying to create a student: {generic_error}",
                 "status": None}
