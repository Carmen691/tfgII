import pandas as pd
import data.querys as qr


def cargar_datos(tipo_entidad_sel, entidades_sel, principios, versiones, niveles, version_aud):
    idioma = pd.DataFrame(qr.obtener_idioma(), columns=["id", "codigo", "nombre"])
    usuarios = pd.DataFrame(qr.obtener_usuarios(), columns=["id", "usuario"])
    auditorias = pd.DataFrame(qr.obtener_auditorias(), columns=["id", "nombre", "idversion", "fecha"])
    tipos_wcag = pd.DataFrame(qr.obtener_tipos_wcag())
    principios = pd.DataFrame(qr.obtener_principios())
    niveles = pd.DataFrame(qr.obtener_niveles())
    versiones = pd.DataFrame(qr.obtener_versiones())
    tipos_entidad = pd.DataFrame(qr.obtener_tipos_entidad())
    entidades = pd.DataFrame(qr.obtener_entidades_por_id(version_aud), columns=["id", "nombre", "id_version"])
    escalas = pd.DataFrame(qr.obtener_escalas())


    entidades_ids = list(entidades['id'])

    principios_ids = list(principios['id'])
    principios_sql = f"({','.join(map(str, principios_ids))})"

    versiones_ids = list(versiones['id'])
    versiones_sql = f"({','.join(map(str, versiones_ids))})"

    niveles_ids = list(niveles['id'])
    niveles_sql = f"({','.join(map(str, niveles_ids))})"

    ids = tuple(entidades_sel)
    ids_sql = str(ids).replace(",)", ")")
    datos = pd.DataFrame(
        qr.obtener_datos(ids_sql, principios_sql, versiones_sql, niveles_sql, version_aud),
        columns=[
            "id_medicion","id_principio","principio","id_entidad","entidad",
            "id_criterio","criterio","id_descripcion","descripcion",
            "observaciones","version"
        ]
    )

    df_datos = pd.DataFrame({
        "Id":datos["id_medicion"],
        "Criterios": datos["criterio"],
        "Valores": datos["id_descripcion"],
        "Entidades": datos["entidad"],
    })

    df_datos["Entidades"] = df_datos["Entidades"].astype(str)

    return {
        "idioma": idioma.to_dict('records'),
        "entidades": entidades.to_dict('records'),
        "usuarios": usuarios.to_dict('records'),
        "auditorias": auditorias.to_dict('records'),
        "datos": datos.to_dict('records'),
        "df_datos": df_datos.to_dict('records'),
        "tiposEntidad": tipos_entidad.to_dict('records'),
        "tiposWCAG": tipos_wcag.to_dict('records'),
        "principios": principios.to_dict('records'),
        "niveles": niveles.to_dict('records'),
        "escalas": escalas.to_dict('records')
    }


def cargar_tipo_entidades():
    tipos_entidad = pd.DataFrame(qr.obtener_tipos_entidad())
    return tipos_entidad.to_dict(orient="records"),


def cargar_datos_inicio():
    idioma = pd.DataFrame(qr.obtener_idioma(), columns=["id", "codigo", "nombre"])
    usuarios = pd.DataFrame(qr.obtener_usuarios(), columns=["id", "usuario"])
    auditorias = pd.DataFrame(qr.obtener_auditorias(), columns=["id", "nombre", "idversion", "fecha"])
    tipos_wcag = pd.DataFrame(qr.obtener_tipos_wcag())
    principios = pd.DataFrame(qr.obtener_principios())
    niveles = pd.DataFrame(qr.obtener_niveles())
    versiones = pd.DataFrame(qr.obtener_versiones())
    tipos_entidad = pd.DataFrame(qr.obtener_tipos_entidad())
    version_aud = pd.DataFrame(qr.obtener_versiones_auditoria(tipos_entidad.iloc[0,0]))
    entidades = pd.DataFrame(qr.obtener_entidades_por_id(version_aud.iloc[0,0]), columns=["id", "nombre", "id_version"])
    escalas = pd.DataFrame(qr.obtener_escalas())
    entidades_ids = list(entidades['id'])
    entidades_sql = f"({','.join(map(str, entidades_ids))})"

    principios_ids = list(principios['id'])
    principios_sql = f"({','.join(map(str, principios_ids))})"

    versiones_ids = list(versiones['id'])
    versiones_sql = f"({','.join(map(str, versiones_ids))})"

    niveles_ids = list(niveles['id'])
    niveles_sql = f"({','.join(map(str, niveles_ids))})"

    datos = pd.DataFrame(
        qr.obtener_datos(entidades_sql, principios_sql, versiones_sql, niveles_sql, version_aud.iloc[0,0]),
        columns=[
            "id_medicion","id_principio","principio","id_entidad","entidad",
            "id_criterio","criterio","id_descripcion","descripcion",
            "observaciones","version"
        ]
    )

    df_datos = pd.DataFrame({
        "Id":datos["id_medicion"],
        "Criterios": datos["criterio"],
        "Valores": datos["id_descripcion"],
        "Entidades": datos["entidad"],
    })

    df_datos["Entidades"] = df_datos["Entidades"].astype(str)

    return {
        "idioma": idioma.to_dict('records'),
        "entidades": entidades.to_dict('records'),
        "usuarios": usuarios.to_dict('records'),
        "auditorias": auditorias.to_dict('records'),
        "datos": datos.to_dict('records'),
        "df_datos": df_datos.to_dict('records'),
        "tiposEntidad": tipos_entidad.to_dict('records'),
        "tiposWCAG": tipos_wcag.to_dict('records'),
        "principios": principios.to_dict('records'),
        "niveles": niveles.to_dict('records'),
        "escalas": escalas.to_dict('records')
    }