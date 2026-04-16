import os

from sqlalchemy import create_engine


def get_db_connection():
    # Reemplaza con tus credenciales
    DATABASE_URL = f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}"

    # Crear conexion
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()

    return conn