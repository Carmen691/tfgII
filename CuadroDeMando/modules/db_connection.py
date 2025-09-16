from sqlalchemy import create_engine


def get_db_connection():
    # Reemplaza con tus credenciales
    DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/dashboard"

    # Crear conexion
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()

    return conn