import os


from sqlalchemy import create_engine


def create_engine_data()->"create_engine":
    """server conection

    Raises:
        ex: if the server raise an exception

    Returns:
        create_engine: server engine instance
    """
    try:
        engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))
    except Exception as ex:
        raise ex
    return engine
