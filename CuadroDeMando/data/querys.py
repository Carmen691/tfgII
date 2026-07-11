import re
import bcrypt
import pandas as pd
from sqlalchemy import create_engine, text
import os


DATABASE_URL = f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:3306/{os.environ['DB_NAME']}"

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_recycle=1800,
    pool_pre_ping=True
)

def obtener_opciones_filtros():
    with engine.begin() as conn:
        result = conn.execute(text("""SELECT DISTINCT
                p.id AS id_principio,
                v.id AS id_version,
                n.id AS id_nivel
                FROM criterios_wcag c
                JOIN criterio_version cv ON c.id = cv.id_criterio 
                JOIN niveles n ON n.id = c.nivel
                JOIN pautas pa ON pa.id = c.id_pauta
                JOIN principios p ON p.id = pa.id_principio
                JOIN versiones_wcag v ON v.id = cv.id_version;"""))
        datos = result.fetchall()
        return datos

def registrar_auditoria(usuario, accion, descripcion):
    datos = [{'usuario': usuario, 'accion': accion, 'descripcion': descripcion}]
    with engine.begin() as conn:
        sql = text("INSERT INTO auditoria (usuario, accion, descripcion) VALUES (:usuario, :accion, :descripcion)")
        conn.execute(sql, datos)

def obtener_idioma():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM idiomas"))
        datos = result.fetchall()
        return datos

def obtener_entidades():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM entidades"))
        datos = result.fetchall()
        return datos


def obtener_numero_entidades(entidades):
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT count(1) FROM entidades where id in {entidades}"))
        datos = result.fetchall()
        return datos[0][0]

def obtener_numero_mediciones(entidades):
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT count(1) FROM dashboard.mediciones_wcag where id_entidad in {entidades}"))
        datos = result.fetchall()
        return datos[0][0]

def obtener_numero_cumplimientos(entidades):
    with engine.begin() as conn:
        result = conn.execute(text(f"""
                SELECT COUNT(m.id)
                FROM dashboard.mediciones_wcag m
                JOIN entidades ent
                    ON ent.id = m.id_entidad
                JOIN versiones ver
                    ON ver.id = ent.id_version
                JOIN escala_valores ev
                    ON ev.id_escala = ver.id_escala
                AND ev.id_descripcion = m.medicion
                WHERE ent.id IN {entidades}
                AND ev.descripcion IN ('Ampliamente conseguido', 'Totalmente conseguido');"""))
        datos = result.fetchall()
        return datos[0][0]

def obtener_porcentaje_cumplimiento(entidades):
    num = obtener_numero_cumplimientos(entidades)
    den = obtener_numero_mediciones(entidades)
    return round(100*(num/den), 2)
    

def obtener_usuarios():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT id, usuario FROM usuarios"))
        datos = result.fetchall()
        return datos

def obtener_auditorias():
    with engine.begin() as conn:
        result = conn.execute(text("""SELECT
                t.id AS id_tipo,
                t.nombre,
                v.id AS id_version,
                v.fecha
            FROM tipos_entidad t
            JOIN versiones v
                ON v.id_tipo_entidad = t.id
            ORDER BY t.nombre, v.fecha DESC
        """))
        datos = result.fetchall()
        return datos
    
def obtener_versiones_auditoria(auditoria):
    with engine.begin() as conn:
        result = conn.execute(text(f"""SELECT
                id AS id_version,
                fecha
                FROM versiones
                WHERE id_tipo_entidad = {auditoria}
            ORDER BY fecha DESC
        """))
        datos = result.fetchall()
        return datos
        
def obtener_escala_tipo_auditoria(auditoria):
    with engine.begin() as conn:
        result = conn.execute(text(f"""SELECT
                id_escala
                FROM versiones
                WHERE id_tipo_entidad = {auditoria}
            ORDER BY fecha DESC
        """))
        datos = result.fetchall()
        return datos
        

def eliminar_auditoria(auditoria, version):
    with engine.begin() as conn:

        conn.execute(text("""
            DELETE FROM dashboard.mediciones_wcag
            WHERE id_entidad IN (
                SELECT id FROM dashboard.entidades
                WHERE id_version = :id_version
            )
        """), {"id_version": version})

        conn.execute(text("""
            DELETE FROM dashboard.entidades
            WHERE id_version = :id_version
        """), {"id_version": version})

        conn.execute(text("""
            DELETE FROM dashboard.versiones
            WHERE id = :version
        """), {"version":version})

        conn.execute(text("""
            DELETE FROM dashboard.tipos_entidad
            WHERE id = :auditoria
        """), {"auditoria": auditoria})


def obtener_pwd(username):
    with engine.begin() as conn:
        result = conn.execute(text(f"Select pwd from usuarios where usuario = '{username}'"))
        datos = result.fetchall()
        return datos[0][0]
    
def actualizar_password(username, passwd):

    query = text("""
        UPDATE usuarios
        SET pwd = :password
        WHERE usuario = :username
    """)

    passwd_bytes = passwd.encode("utf-8")
    pwd_converted = bcrypt.hashpw(passwd_bytes, bcrypt.gensalt())
    with engine.begin() as conn:

        result = conn.execute(
            query,
            {
                "password": pwd_converted,
                "username": username
            }
        )

    return result.rowcount
    
def obtener_admin(username):
    with engine.begin() as conn:
        result = conn.execute(text(f"Select es_admin from usuarios where usuario = '{username}'"))
        datos = result.fetchall()
        return datos[0][0]

def existe_usuario(username):
    with engine.begin() as conn:
        result = conn.execute(text(f"Select usuario from usuarios where usuario = '{username}'"))
        datos = result.rowcount
        return datos


def obtener_datos(entidades, principios, versiones, niveles, version):
    with engine.begin() as conn:
        consulta = """SELECT m.id as id_medicion, p.id AS id_principio, COALESCE(pt.texto, p.nombre) AS principio,
            e.id AS id_entidad, e.nombre AS entidad, c.id AS id_criterio,
            COALESCE(ct.texto, c.nombre) AS criterio, ev.id_descripcion as id_descripcion, ev.descripcion,
            m.observaciones, v.version FROM mediciones_wcag m
            JOIN entidades e ON m.id_entidad = e.id"""
            
        if entidades:
            consulta += f""" and e.id in {entidades}"""

        consulta += """ JOIN criterios_wcag c ON m.id_criterio = c.id
            JOIN niveles n ON c.nivel = n.id"""
        
        if niveles:
            consulta += f""" and n.id in {niveles}"""
            
        consulta += """ JOIN pautas pa ON c.id_pauta = pa.id
            JOIN principios p ON pa.id_principio = p.id"""
            
        if principios:
            consulta += f""" and p.id in {principios}"""
            
        consulta += """ JOIN versiones ver 
                    on ver.id = e.id_version
                    JOIN criterio_version cv on c.id = cv.id_criterio
                    JOIN versiones_wcag v on v.id = cv.id_version"""
            
        if versiones:
            consulta += f""" and v.id in {versiones}"""    
        else:
            consulta += f" AND v.id = ver.id_version"
        
        if version:
            consulta += f""" and ver.id = {version}"""
            
        consulta += """ JOIN escala_valores ev ON ev.id_escala = ver.id_escala
            AND ev.id_descripcion = m.medicion
            LEFT JOIN traducciones pt ON p.id = pt.id_elemento 
            AND pt.tabla = 'principios' AND pt.campo = 'nombre' 
            AND pt.id_idioma = (SELECT id FROM idiomas WHERE codigo = 'ES')
            LEFT JOIN traducciones ct ON c.id = ct.id_elemento 
            AND ct.tabla = 'criterios_wcag' AND ct.campo = 'nombre' 
            AND ct.id_idioma = (SELECT id FROM idiomas WHERE codigo = 'ES')
            ORDER BY p.id, e.id, c.id;"""
        result = conn.execute(text(consulta))
        datos = result.fetchall()
        return datos


def obtener_suma_cumplimiento(entidades, principios, versiones, niveles, version):
    with engine.begin() as conn:

        # Obtener la escala de la versión
        id_escala = conn.execute(
            text("SELECT id_escala FROM versiones WHERE id = :version"),
            {"version": version}
        ).scalar()

        # Obtener los valores de esa escala
        valores = conn.execute(
            text("""
                SELECT id_descripcion, descripcion
                FROM escala_valores
                WHERE id_escala = :id_escala
                ORDER BY id_descripcion
            """),
            {"id_escala": id_escala}
        ).fetchall()

        columnas = []

        for id_desc, descripcion in valores:
            alias = (
                descripcion.lower()
                .replace(" ", "_")
                .replace("á", "a")
                .replace("é", "e")
                .replace("í", "i")
                .replace("ó", "o")
                .replace("ú", "u")
            )

            columnas.append(
                f"SUM(CASE WHEN m.medicion = {id_desc} THEN 1 ELSE 0 END) AS {alias}"
            )

        consulta = f"""
        SELECT
            p.nombre AS principio,
            {', '.join(columnas)}
        FROM mediciones_wcag m
        JOIN entidades ent ON ent.id = m.id_entidad
        """

        if entidades:
            consulta += f" AND ent.id IN {entidades}"

        consulta += """
        JOIN criterios_wcag c ON m.id_criterio = c.id
        JOIN niveles n ON c.nivel = n.id
        """

        if niveles:
            consulta += f" AND n.id IN {niveles}"

        consulta += """
        JOIN pautas pa ON c.id_pauta = pa.id
        JOIN principios p ON pa.id_principio = p.id
        """

        if principios:
            consulta += f" AND p.id IN {principios}"

        consulta += """
        JOIN versiones ver ON ver.id = ent.id_version
        JOIN criterio_version cv ON c.id = cv.id_criterio
        JOIN versiones_wcag v ON v.id = cv.id_version
        """

        if versiones:
            consulta += f" AND v.id IN {max(versiones)}"

        if version:
            consulta += f" AND ver.id = {version}"

        consulta += """
        JOIN escala_valores ev
            ON ev.id_escala = ver.id_escala
           AND ev.id_descripcion = m.medicion
        LEFT JOIN traducciones pt
            ON p.id = pt.id_elemento
           AND pt.tabla = 'principios'
           AND pt.campo = 'nombre'
           AND pt.id_idioma = (
                SELECT id
                FROM idiomas
                WHERE codigo = 'ES'
           )
        GROUP BY p.nombre
        ORDER BY p.nombre
        """

        result = conn.execute(text(consulta))
        return result.fetchall(), result.keys()

def obtener_mapa_calor():
    with engine.begin() as conn:
        result = conn.execute(text("""SELECT 
                c.codigo AS codigo_criterio,
                c.nombre AS nombre_criterio,
                p.codigo AS codigo_pauta,
                p.nombre AS nombre_pauta,
                pr.nombre AS nombre_principio,
                SUM(CASE WHEN m.medicion = 1 THEN 1 ELSE 0 END) AS no_conseguido,
                SUM(CASE WHEN m.medicion = 2 THEN 1 ELSE 0 END) AS parcialmente_conseguido,
                SUM(CASE WHEN m.medicion = 3 THEN 1 ELSE 0 END) AS no_aplicable,
                SUM(CASE WHEN m.medicion = 4 THEN 1 ELSE 0 END) AS ampliamente_conseguido,
                SUM(CASE WHEN m.medicion = 5 THEN 1 ELSE 0 END) AS totalmente_conseguido
                FROM 
                mediciones_wcag m
                INNER JOIN 
                criterios_wcag c ON m.id_criterio = c.id
                INNER JOIN 
                pautas p ON c.id_pauta = p.id
                INNER JOIN 
                principios pr ON p.id_principio = pr.id
                GROUP BY 
                c.codigo, c.nombre, p.codigo, p.nombre, pr.nombre
                ORDER BY 
                c.codigo;"""))
        datos = result.fetchall()
        return datos

def obtener_opciones_cumplimiento(idioma, id):
    with engine.begin() as conn:
        result = conn.execute(text(f"""SELECT id_descripcion, descripcion FROM dashboard.escala_valores where id_escala = {id};"""))
        datos = result.fetchall()
        return datos


def obtener_escalas():
    with engine.begin() as conn:
        result = conn.execute(text(""" SELECT id, descripcion FROM escalas;"""))
        datos = result.fetchall()
        return datos

def obtener_tipos_entidad():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM tipos_entidad"))
        datos = result.fetchall()
        return datos
    
def obtener_tipos_entidad_por_id(id):
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT nombre FROM tipos_entidad where id = {id}"))
        datos = result.fetchall()
        return datos
    
def obtener_version_por_id_entidad(id):
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT version FROM versiones_wcag where id = (Select id_version from versiones where id_tipo_entidad = {id})"))
        datos = result.fetchall()
        return datos

def obtener_tipos_wcag():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT id, version FROM versiones_wcag"))
        datos = result.fetchall()
        return datos

def obtener_principios():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT id, nombre FROM principios"))
        datos = result.fetchall()
        return datos

def obtener_cumplimiento_principios(entidades, principios, versiones, niveles, version):
        
    sql = """SELECT p.nombre,
            SUM(CASE
                WHEN ev.descripcion IN ('Ampliamente conseguido', 'Totalmente conseguido')
                THEN med.medicion ELSE 0 END) * 1.0
            / SUM(med.medicion) * 100 AS porcentaje
            FROM mediciones_wcag med INNER JOIN entidades ent ON med.id_entidad = ent.id"""

    if entidades:
        sql += f" and ent.id in {entidades}"

    sql += """ JOIN criterios_wcag c ON med.id_criterio = c.id
            JOIN niveles n ON c.nivel = n.id """

    if niveles:
        sql += f" and n.id in {niveles}"

    sql += """ JOIN pautas pa ON c.id_pauta = pa.id
            JOIN principios p ON pa.id_principio = p.id"""

    if principios:
        sql += f" and p.id in {principios}"

    sql += """ JOIN versiones ver 
            on ver.id = ent.id_version
			JOIN criterio_version cv on c.id = cv.id_criterio
            JOIN versiones_wcag v on v.id = cv.id_version"""

    if versiones:
        sql += f" and v.id in {versiones}"
    
    if version:
        sql += f""" and ver.id = {version}"""

    sql += """ JOIN escala_valores ev ON ev.id_escala = ver.id_escala
            AND ev.id_descripcion = med.medicion
            LEFT JOIN traducciones pt ON p.id = pt.id_elemento 
            AND pt.tabla = 'principios' AND pt.campo = 'nombre'
            AND pt.id_idioma = (SELECT id FROM idiomas WHERE codigo = 'ES')
            LEFT JOIN traducciones ct ON c.id = ct.id_elemento 
            AND ct.tabla = 'criterios_wcag' AND ct.campo = 'nombre' 
            AND ct.id_idioma = (SELECT id FROM idiomas WHERE codigo = 'ES')
            ORDER BY p.nombre"""

    with engine.begin() as conn:
        result = conn.execute(text(sql))
        datos = result.fetchall()
        return datos


def obtener_cumplimiento_niveles(entidades, principios, versiones, niveles, version):
                
    sql = """SELECT 
            n.nombre,
            SUM(CASE
                WHEN ev.descripcion IN ('Ampliamente conseguido', 'Totalmente conseguido')
                THEN med.medicion ELSE 0 END) * 1.0
            / SUM(med.medicion) * 100 AS porcentaje
            FROM mediciones_wcag med
            INNER JOIN entidades ent ON med.id_entidad = ent.id"""
  
    if entidades:
        sql += f""" and ent.id in {entidades}"""

    sql += """ JOIN criterios_wcag c ON med.id_criterio = c.id
            JOIN niveles n ON c.nivel = n.id """
 
    if niveles:
        sql += f""" and n.id in {niveles}"""

    sql += """ JOIN pautas pa ON c.id_pauta = pa.id
            JOIN principios p ON pa.id_principio = p.id"""
    
    if principios:
        sql += f""" and p.id in {principios}"""

    sql += """ JOIN versiones ver 
            on ver.id = ent.id_version
			JOIN criterio_version cv on c.id = cv.id_criterio
            JOIN versiones_wcag v on v.id = cv.id_version"""

    if versiones:
        sql += f""" and v.id in {versiones}"""

    if version:
        sql += f""" and ver.id = {version}"""
    
    sql += """ JOIN escala_valores ev ON ev.id_escala = ver.id_escala
            AND ev.id_descripcion = med.medicion
            LEFT JOIN traducciones pt ON p.id = pt.id_elemento 
            AND pt.tabla = 'principios' AND pt.campo = 'nombre'
            AND pt.id_idioma = (SELECT id FROM idiomas WHERE codigo = 'ES')
            LEFT JOIN traducciones ct ON c.id = ct.id_elemento 
            AND ct.tabla = 'criterios_wcag' AND ct.campo = 'nombre' 
            AND ct.id_idioma = (SELECT id FROM idiomas WHERE codigo = 'ES') GROUP BY n.nombre"""


    with engine.begin() as conn:
        result = conn.execute(text(sql))
        datos = result.fetchall()
        return datos

def obtener_niveles():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM niveles"))
        datos = result.fetchall()
        return datos

def obtener_versiones():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * from versiones_wcag"))
        datos = result.fetchall()
        return datos

def guardar_nuevo_tipo_entidad(conn, valor_input, valor_escala, fecha, version):
    result = conn.execute(text(f"SELECT * FROM tipos_entidad where nombre = '{valor_input}'"))
    fila = result.fetchone()
    if fila:
        id_tipo = fila.id
        result = conn.execute(text(f"""SELECT id FROM versiones
            WHERE id_tipo_entidad = (Select id from tipos_entidad where nombre = '{valor_input}') AND fecha = '{fecha}' AND id_escala = '{valor_escala}'"""))
        if result.rowcount > 0:
            return 0
        else: 
            result = conn.execute(text(f"""INSERT INTO versiones (id_tipo_entidad, fecha, id_escala, id_version) VALUES (:id_tipo, :fecha, :escala, :version)"""), {"id_tipo": id_tipo, "fecha": fecha, "escala": valor_escala, "version":version})
            return result.lastrowid
    else:
        result = conn.execute(text(f"INSERT INTO tipos_entidad (nombre) VALUES (:valor)"), {"valor": valor_input})
        result = conn.execute(text(f"""INSERT INTO versiones (id_tipo_entidad, fecha, id_escala) VALUES (:id_tipo, :fecha, :escala)"""), {"id_tipo": result.lastrowid, "fecha": fecha, "escala": valor_escala})
        return result.lastrowid

def guardar_entidades(conn, id_version, columnas_limpias):
    # Preparar datos para inserción masiva
    datos = [{'nombre': nombre, 'id_version': id_version} for nombre in columnas_limpias]

    # Insertar datos con executemany
    sql = text("INSERT INTO entidades (nombre, id_version) VALUES (:nombre, :id_version)")
    result = conn.execute(sql, datos)
    return result.rowcount


def obtener_entidades_por_id(id_version):
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT * FROM entidades where id_version = {id_version}"))
        datos = result.fetchall()
        return datos

def obtener_entidades_por_nombre(id_tipo):
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT * FROM entidades where id_version = (SELECT id from versiones where id_tipo_entidad = '{id_tipo}')"))
        datos = result.fetchall()
        return datos


def guardar_valores(conn, id_version, df):

    result = conn.execute(text(f"SELECT * FROM entidades where id_version = {id_version}"))
    entidades = result.fetchall()

    # Cargar todos los criterios una sola vez

    result = conn.execute(text("""
        SELECT id, codigo
        FROM dashboard.criterios_wcag
    """))

    criterios = {
        row.codigo: row.id
        for row in result
    }

    datos = []

    try:
        for row in df.itertuples(index=False):

            # Primera columna
            if pd.isna(row[0]):
                continue

            codigo = re.split(r'[ :]', str(row[1]))[0]

            id_criterio = criterios.get(codigo)

            if id_criterio is None:
                continue
            
            j = 0
            for i, dato in enumerate(row):
                if isinstance(dato, (int, float)):

                    datos.append({
                        "id_entidad": entidades[j][0],
                        "id_criterio": id_criterio,
                        "medicion": dato
                    })
                    j = j+1
    except Exception as e:
        print("ERROR:", repr(e))
        raise

    if not datos:
        return

    sql = text("""
        INSERT INTO mediciones_wcag (
            id_entidad,
            id_criterio,
            medicion
        )
        VALUES (
            :id_entidad,
            :id_criterio,
            :medicion
        )
    """)

    result = conn.execute(sql, datos)
    return result.rowcount

def obtener_criterio(codigo):
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT id FROM dashboard.criterios_wcag where codigo = '{codigo}'"))
        dato = result.fetchone()
        return dato[0]

def guardar_nuevo_usuario(usuario, passwd, admin):
    with engine.begin() as conn:

        existe_usuario = text(f"SELECT COUNT(*) FROM usuarios WHERE usuario = '{usuario}'")
        result = conn.execute(existe_usuario, {"usuario": usuario}).scalar()

        if admin:
            admin = 1
        else:
            admin = 0

        if result > 0:
            return False
        
        passwd_bytes = passwd.encode("utf-8")
        pwd_converted = bcrypt.hashpw(passwd_bytes, bcrypt.gensalt())
        # Preparar datos para inserción masiva
        datos = [{'usuario': usuario, 'pwd': pwd_converted, 'es_admin': admin}]
        # Insertar datos con executemany
        sql = text("INSERT INTO usuarios (usuario, pwd, es_admin) VALUES (:usuario, :pwd, :es_admin)")
        resultado = conn.execute(sql, datos)
        return resultado.rowcount



def eliminar_usuario(usuario):
    with engine.begin() as conn:

        datos = [{'usuario': usuario}]
        sql = text("delete from usuarios where usuario = :usuario")
        conn.execute(sql, datos)
        result = conn.execute(sql, datos)


def obtener_textos_interfaz(idioma_codigo, seccion, clave):
    """
    Devuelve el texto dependiendo del idioma seleccionado
    """
    with engine.begin() as conn:
        result = conn.execute(text(f"""SELECT ui.texto FROM traducciones_ui ui
                JOIN idiomas i ON i.id = ui.id_idioma
                WHERE i.codigo = '{idioma_codigo}' 
                AND ui.seccion = '{seccion}' AND ui.clave = '{clave}'"""))
        dato = result.fetchone()
        return dato[0]

        
def actualizar_datos_mediciones(tuplas_update):
    """
    Actualiza los datos de mediciones
    """
    result = -1
    query = text("""
        UPDATE mediciones_wcag
        SET medicion = :medicion
        WHERE id = :id""")

    with engine.begin() as conn:
        result = conn.execute(query, [
            {"medicion": v, "id": i}
            for v, i in tuplas_update
        ])
        result = result.rowcount
    return result