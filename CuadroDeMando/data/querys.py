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


def obtener_numero_entidades(tipo_entidad):
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT count(1) FROM entidades where id_tipo = '{tipo_entidad}'"))
        datos = result.fetchall()
        return datos[0][0]

def obtener_numero_mediciones(tipo_entidad):
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT count(1) FROM dashboard.mediciones_wcag where id_entidad in (Select id from entidades where id_tipo = '{tipo_entidad}')"))
        datos = result.fetchall()
        return datos[0][0]

def obtener_numero_cumplimientos(tipo_entidad):
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT count(id) FROM dashboard.mediciones_wcag where id_entidad in (Select id from entidades where id_tipo = '{tipo_entidad}') and medicion in (4,5);"))
        datos = result.fetchall()
        return datos[0][0]

def obtener_porcentaje_cumplimiento(tipo_entidad):
    num = obtener_numero_cumplimientos(tipo_entidad)
    den = obtener_numero_mediciones(tipo_entidad)
    return round(100*(num/den), 2)
    

def obtener_usuarios():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT id, usuario FROM usuarios"))
        datos = result.fetchall()
        return datos

def obtener_auditorias():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT id, nombre FROM tipos_entidad"))
        datos = result.fetchall()
        return datos

def eliminar_auditoria(auditoria):
    with engine.begin() as conn:

        conn.execute(text("""
            DELETE FROM dashboard.mediciones_wcag
            WHERE id_entidad IN (
                SELECT id FROM dashboard.entidades
                WHERE nombre = :auditoria
            )
        """), {"auditoria": auditoria})

        conn.execute(text("""
            DELETE FROM dashboard.entidades
            WHERE id_tipo = (
                SELECT id FROM dashboard.tipos_entidad
                WHERE nombre = :auditoria
            )
        """), {"auditoria": auditoria})

        conn.execute(text("""
            DELETE FROM dashboard.tipos_entidad
            WHERE nombre = :auditoria
        """), {"auditoria": auditoria})


def obtener_pwd(username):
    with engine.begin() as conn:
        result = conn.execute(text(f"Select pwd from usuarios where usuario = '{username}'"))
        datos = result.fetchall()
        return datos[0][0]

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


def obtener_datos(entidades, principios, versiones, niveles):
    with engine.begin() as conn:
        result = conn.execute(text(f"""SELECT p.id AS id_principio, COALESCE(pt.texto, p.nombre) AS principio,
            e.id AS id_entidad, e.nombre AS entidad, c.id AS id_criterio,
            COALESCE(ct.texto, c.nombre) AS criterio, ev.id_escala as id_descripcion, ev.descripcion,
            m.observaciones, v.version FROM mediciones_wcag m
            JOIN entidades e ON m.id_entidad = e.id
            and e.id in {entidades}
            JOIN criterios_wcag c ON m.id_criterio = c.id
            JOIN niveles n ON c.nivel = n.id
            and n.id in {niveles}
            JOIN pautas pa ON c.id_pauta = pa.id
            JOIN principios p ON pa.id_principio = p.id
            and p.id in {principios}
            JOIN versiones_wcag v ON m.id_version = v.id
            and v.id in {versiones}
            JOIN escala_valores ev ON ev.id_escala = m.medicion
            LEFT JOIN traducciones pt ON p.id = pt.id_elemento 
            AND pt.tabla = 'principios' AND pt.campo = 'nombre' 
            AND pt.id_idioma = (SELECT id FROM idiomas WHERE codigo = 'ES')
            LEFT JOIN traducciones ct ON c.id = ct.id_elemento 
            AND ct.tabla = 'criterios_wcag' AND ct.campo = 'nombre' 
            AND ct.id_idioma = (SELECT id FROM idiomas WHERE codigo = 'ES')
            ORDER BY p.id, e.id, c.id;"""))
        datos = result.fetchall()
        return datos

def obtener_suma_cumplimiento():
    with engine.begin() as conn:
        result = conn.execute(text("""SELECT 
                p.nombre AS principio,
                SUM(CASE WHEN m.medicion = 1 THEN 1 ELSE 0 END) AS num_no_conseguido,
                SUM(CASE WHEN m.medicion = 2 THEN 1 ELSE 0 END) AS num_parcialmente_conseguido,
                SUM(CASE WHEN m.medicion = 3 THEN 1 ELSE 0 END) AS num_no_aplicable,
                SUM(CASE WHEN m.medicion = 4 THEN 1 ELSE 0 END) AS num_ampliamente_conseguido,
                SUM(CASE WHEN m.medicion = 5 THEN 1 ELSE 0 END) AS num_totalmente_conseguido
                FROM 
                mediciones_wcag m
                JOIN criterios_wcag c ON m.id_criterio = c.id
                JOIN pautas pa ON c.id_pauta = pa.id
                JOIN principios p ON pa.id_principio = p.id
                GROUP BY 
                p.id, p.nombre
                ORDER BY 
                p.nombre;"""))
        datos = result.fetchall()
        return datos


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

def obtener_opciones_cumplimiento():
    with engine.begin() as conn:
        result = conn.execute(text("""SELECT id_escala, descripcion FROM dashboard.escala_valores;"""))
        datos = result.fetchall()
        return datos

def obtener_tipos_entidad():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM tipos_entidad"))
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

def obtener_cumplimiento_principios(tipoEntidad):
    with engine.begin() as conn:
        result = conn.execute(text(f"""SELECT 
            pri.nombre,
            SUM(CASE WHEN med.medicion IN (4, 5) THEN med.medicion ELSE 0 END) * 1.0
            / SUM(med.medicion) * 100 AS porcentaje
            FROM mediciones_wcag med
            INNER JOIN entidades ent ON med.id_entidad = ent.id
            INNER JOIN tipos_entidad ten ON ent.id_tipo = ten.id
            and ten.id = {tipoEntidad}
            INNER JOIN criterios_wcag cri ON med.id_criterio = cri.id
            INNER JOIN pautas pau ON cri.id_pauta = pau.id
            INNER JOIN principios pri ON pau.id_principio = pri.id
            GROUP BY pri.nombre;"""))
        datos = result.fetchall()
        return datos


def obtener_cumplimiento_niveles(tipoEntidad):
    with engine.begin() as conn:
        result = conn.execute(text(f"""SELECT 
            niv.nombre,
            SUM(CASE WHEN med.medicion IN (4, 5) THEN med.medicion ELSE 0 END) * 1.0
            / SUM(med.medicion) * 100 AS porcentaje
            FROM mediciones_wcag med
            INNER JOIN entidades ent ON med.id_entidad = ent.id
            INNER JOIN tipos_entidad ten ON ent.id_tipo = ten.id
            and ent.id = {tipoEntidad}
            INNER JOIN criterios_wcag cri ON med.id_criterio = cri.id
            INNER JOIN niveles niv ON cri.nivel = niv.id
            INNER JOIN pautas pau ON cri.id_pauta = pau.id
            INNER JOIN principios pri ON pau.id_principio = pri.id
            GROUP BY niv.nombre;"""))
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

def guardar_nuevo_tipo_entidad(valor_input):
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT * FROM tipos_entidad where nombre = '{valor_input}'"))
        if result.rowcount > 0:
            return result.rowcount
        else:
            result = conn.execute(text("INSERT INTO tipos_entidad (nombre) VALUES (:valor)"), {"valor": valor_input})
            return result.rowcount

def guardar_entidades(id_tipo, columnas_limpias):
    with engine.begin() as conn:

        # Preparar datos para inserción masiva
        datos = [{'nombre': nombre, 'id_tipo': id_tipo} for nombre in columnas_limpias]

        # Insertar datos con executemany
        sql = text("INSERT INTO entidades (nombre, id_tipo) VALUES (:nombre, :id_tipo)")
        conn.execute(sql, datos)


def obtener_entidades_por_id(id_entidad):
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT * FROM entidades where id_tipo = {id_entidad}"))
        datos = result.fetchall()
        return datos

def obtener_entidades_por_nombre(id_entidad):
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT * FROM entidades where id_tipo = '{id_entidad}'"))
        datos = result.fetchall()
        return datos

def guardar_valores(id_tipo, id_wcag, df):
    entidades = obtener_entidades_por_id(id_tipo)

    datos = []
    for idx, row in df.iterrows():
        fila_valida = row[0]
        if not pd.isna(fila_valida):
            i = 0
            for dato in row:
                if isinstance(dato, (int,float)):
                    id_criterio = obtener_criterio(re.split(r'[ :]', row[1])[0])
                    id_version = id_wcag
                    id_entidad = entidades[i][0]
                    valor = dato
                    datos.append({
                        'id_entidad': id_entidad,
                        'id_criterio': id_criterio,
                        'id_version' : id_version,
                        'medicion': dato
                    })
                    i = i+1


    # Inserción masiva
    with engine.begin() as conn:
        sql = text("""
            INSERT INTO mediciones_wcag (id_entidad, id_criterio, id_version, medicion)
            VALUES (:id_entidad, :id_criterio, :id_version, :medicion)
        """)
        conn.execute(sql, datos)


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
        conn.execute(sql, datos)



def eliminar_usuario(usuario):
    with engine.begin() as conn:

        datos = [{'usuario': usuario}]
        sql = text("delete from usuarios where usuario = :usuario")
        conn.execute(sql, datos)



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

        
