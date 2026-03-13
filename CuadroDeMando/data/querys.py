import re
import bcrypt
import pandas as pd
from modules.db_connection import get_db_connection
from sqlalchemy import create_engine, text


def obtener_idioma():
    conn = get_db_connection()
    result = conn.execute(text("SELECT * FROM idiomas"))
    datos = result.fetchall()
    conn.close()
    return datos

def obtener_entidades():
    conn = get_db_connection()
    result = conn.execute(text("SELECT * FROM entidades"))
    datos = result.fetchall()
    conn.close()
    return datos


def obtener_numero_entidades(tipo_entidad):
    conn = get_db_connection()
    result = conn.execute(text(f"SELECT count(1) FROM entidades where id_tipo = (Select id from tipos_entidad where nombre = '{tipo_entidad}')"))
    datos = result.fetchall()
    conn.close()
    return datos[0][0]

def obtener_usuarios():
    conn = get_db_connection()
    result = conn.execute(text("SELECT id, usuario FROM usuarios"))
    datos = result.fetchall()
    conn.close()
    return datos

def obtener_auditorias():
    conn = get_db_connection()
    result = conn.execute(text("SELECT id, nombre FROM tipos_entidad"))
    datos = result.fetchall()
    conn.close()
    return datos

def eliminar_auditoria(auditoria):
    conn = get_db_connection()

    try:
        with conn.begin():  # Inicia transacción automática (también hace commit)
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

    finally:
        conn.close()

def obtener_pwd(username):
    conn = get_db_connection()
    result = conn.execute(text(f"Select pwd from usuarios where usuario = '{username}'"))
    datos = result.fetchall()
    conn.close()
    return datos[0][0]

def obtener_admin(username):
    conn = get_db_connection()
    result = conn.execute(text(f"Select es_admin from usuarios where usuario = '{username}'"))
    datos = result.fetchall()
    conn.close()
    return datos[0][0]

def existe_usuario(username):
    conn = get_db_connection()
    result = conn.execute(text(f"Select usuario from usuarios where usuario = '{username}'"))
    datos = result.rowcount
    conn.close()
    return datos


def obtener_datos():
    conn = get_db_connection()
    result = conn.execute(text("""SELECT p.id AS id_principio, COALESCE(pt.texto, p.nombre) AS principio,
        e.id AS id_entidad, e.nombre AS entidad, c.id AS id_criterio,
        COALESCE(ct.texto, c.nombre) AS criterio, ev.id_escala as id_descripcion, ev.descripcion,
        m.observaciones, v.version FROM mediciones_wcag m
        JOIN entidades e ON m.id_entidad = e.id
        JOIN criterios_wcag c ON m.id_criterio = c.id
        JOIN pautas pa ON c.id_pauta = pa.id
        JOIN principios p ON pa.id_principio = p.id
        JOIN versiones_wcag v ON m.id_version = v.id
        JOIN escala_valores ev ON ev.id_escala = m.medicion
        LEFT JOIN traducciones pt ON p.id = pt.id_elemento 
        AND pt.tabla = 'principios' AND pt.campo = 'nombre' 
        AND pt.id_idioma = (SELECT id FROM idiomas WHERE codigo = 'ES')
        LEFT JOIN traducciones ct ON c.id = ct.id_elemento 
        AND ct.tabla = 'criterios_wcag' AND ct.campo = 'nombre' 
        AND ct.id_idioma = (SELECT id FROM idiomas WHERE codigo = 'ES')
        ORDER BY p.id, e.id, c.id;"""))
    datos = result.fetchall()
    conn.close()
    return datos

def obtener_suma_cumplimiento():
    conn = get_db_connection()
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
    conn.close()
    return datos


def obtener_mapa_calor():
    conn = get_db_connection()
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
    conn.close()
    return datos

def obtener_opciones_cumplimiento():
    conn = get_db_connection()
    result = conn.execute(text("""SELECT id_escala, descripcion FROM dashboard.escala_valores;"""))
    datos = result.fetchall()
    conn.close()
    return datos

def obtener_tipos_entidad():
    conn = get_db_connection()
    result = conn.execute(text("SELECT * FROM tipos_entidad"))
    datos = result.fetchall()
    conn.close()
    return datos

def obtener_tipos_wcag():
    conn = get_db_connection()
    result = conn.execute(text("SELECT id, version FROM versiones_wcag"))
    datos = result.fetchall()
    conn.close()
    return datos

def guardar_nuevo_tipo_entidad(valor_input):
    conn = get_db_connection()
    result = conn.execute(text(f"SELECT * FROM tipos_entidad where nombre = '{valor_input}'"))
    if result.rowcount > 0:
        conn.close()
        return result.rowcount
    else:
        conn.execute(text("INSERT INTO tipos_entidad (nombre) VALUES (:valor)"), {"valor": valor_input})
        conn.commit()
        conn.close()
        return 0
    

def guardar_entidades(id_tipo, columnas_limpias):
    conn = get_db_connection()

    # Preparar datos para inserción masiva
    datos = [{'nombre': nombre, 'id_tipo': id_tipo} for nombre in columnas_limpias]

    # Insertar datos con executemany
    sql = text("INSERT INTO entidades (nombre, id_tipo) VALUES (:nombre, :id_tipo)")
    conn.execute(sql, datos)

    conn.commit()
    conn.close()


def obtener_entidades_por_id(id_entidad):
    conn = get_db_connection()
    result = conn.execute(text(f"SELECT * FROM entidades where id_tipo = {id_entidad}"))
    datos = result.fetchall()
    conn.close()
    return datos

def obtener_entidades_por_nombre(nombre_entidad):
    conn = get_db_connection()
    result = conn.execute(text(f"SELECT * FROM entidades where id_tipo = (Select id from tipos_entidad where nombre = '{nombre_entidad}')"))
    datos = result.fetchall()
    conn.close()
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
    conn = get_db_connection()
    sql = text("""
        INSERT INTO mediciones_wcag (id_entidad, id_criterio, id_version, medicion)
        VALUES (:id_entidad, :id_criterio, :id_version, :medicion)
    """)
    conn.execute(sql, datos)
    conn.commit()
    conn.close()


def obtener_criterio(codigo):
    conn = get_db_connection()
    result = conn.execute(text(f"SELECT id FROM dashboard.criterios_wcag where codigo = '{codigo}'"))
    dato = result.fetchone()
    conn.close()
    return dato[0]

def guardar_nuevo_usuario(usuario, passwd, admin):
    conn = get_db_connection()

    existe_usuario = text(f"SELECT COUNT(*) FROM usuarios WHERE usuario = '{usuario}'")
    result = conn.execute(existe_usuario, {"usuario": usuario}).scalar()

    if admin:
        admin = 1
    else:
        admin = 0

    if result > 0:
        conn.close()
        return False
    
    passwd_bytes = passwd.encode("utf-8")
    pwd_converted = bcrypt.hashpw(passwd_bytes, bcrypt.gensalt())
    # Preparar datos para inserción masiva
    datos = [{'usuario': usuario, 'pwd': pwd_converted, 'es_admin': admin}]
    # Insertar datos con executemany
    sql = text("INSERT INTO usuarios (usuario, pwd, es_admin) VALUES (:usuario, :pwd, :es_admin)")
    conn.execute(sql, datos)

    conn.commit()
    conn.close()


def eliminar_usuario(usuario):
    conn = get_db_connection()

    datos = [{'usuario': usuario}]
    sql = text("delete from usuarios where usuario = :usuario")
    conn.execute(sql, datos)

    conn.commit()
    conn.close()


def obtener_textos_interfaz(idioma_codigo, seccion, clave):
    """
    Devuelve el texto dependiendo del idioma seleccionado
    """
    conn = get_db_connection()
    result = conn.execute(text(f"""SELECT ui.texto FROM traducciones_ui ui
            JOIN idiomas i ON i.id = ui.id_idioma
            WHERE i.codigo = '{idioma_codigo}' 
            AND ui.seccion = '{seccion}' AND ui.clave = '{clave}'"""))
    dato = result.fetchone()
    conn.close()
    return dato[0]

        
