from modules.db_connection import get_db_connection
from sqlalchemy import create_engine, text


def obtener_idioma():
    conn = get_db_connection()
    result = conn.execute(text("SELECT * FROM idiomas"))
    datos = result.fetchall()
    conn.close()
    return datos

def obtener_tipos_entidad():
    conn = get_db_connection()
    result = conn.execute(text("SELECT * FROM entidades"))
    datos = result.fetchall()
    conn.close()
    return datos

def obtener_datos():
    conn = get_db_connection()
    result = conn.execute(text("""SELECT p.id AS id_principio, COALESCE(pt.texto, p.nombre) AS principio,
        e.id AS id_entidad, e.nombre AS entidad, c.id AS id_criterio,
        COALESCE(ct.texto, c.nombre) AS criterio, ev.descripcion,
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