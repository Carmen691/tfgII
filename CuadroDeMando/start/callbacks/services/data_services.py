import pandas as pd
import data.querys as qr


def cargar_datos(tipo_entidad, entidades, principios, versiones, niveles):
    idioma = pd.DataFrame(qr.obtener_idioma(), columns=["id", "codigo", "nombre"])
    usuarios = pd.DataFrame(qr.obtener_usuarios(), columns=["id", "usuario"])
    auditorias = pd.DataFrame(qr.obtener_auditorias(), columns=["id", "nombre"])
    tipos_wcag = pd.DataFrame(qr.obtener_tipos_wcag())
    principios = pd.DataFrame(qr.obtener_principios())
    niveles = pd.DataFrame(qr.obtener_niveles())
    versiones = pd.DataFrame(qr.obtener_versiones())
    tipos_entidad = pd.DataFrame(qr.obtener_tipos_entidad())
    entidades = pd.DataFrame(qr.obtener_entidades_por_id(tipos_entidad.iloc[0,0]), columns=["id", "nombre", "id_tipo"])


    entidades_ids = list(entidades['id'])
    entidades_sql = f"({','.join(map(str, entidades_ids))})"

    principios_ids = list(principios['id'])
    principios_sql = f"({','.join(map(str, principios_ids))})"

    versiones_ids = list(versiones['id'])
    versiones_sql = f"({','.join(map(str, versiones_ids))})"

    niveles_ids = list(niveles['id'])
    niveles_sql = f"({','.join(map(str, niveles_ids))})"

    datos = pd.DataFrame(
        qr.obtener_datos(entidades_sql, principios_sql, versiones_sql, niveles_sql),
        columns=[
            "id_principio","principio","id_entidad","entidad",
            "id_criterio","criterio","id_descripcion","descripcion",
            "observaciones","version"
        ]
    )

    df_datos = pd.DataFrame({
        "Criterios": datos["criterio"],
        "Valores": datos["descripcion"],
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
        "niveles": niveles.to_dict('records')
    }


def cargar_tipo_entidades():
    tipos_entidad = pd.DataFrame(qr.obtener_tipos_entidad())
    return tipos_entidad.to_dict(orient="records"),


def cargar_datos_inicio():
    idioma = pd.DataFrame(qr.obtener_idioma(), columns=["id", "codigo", "nombre"])
    usuarios = pd.DataFrame(qr.obtener_usuarios(), columns=["id", "usuario"])
    auditorias = pd.DataFrame(qr.obtener_auditorias(), columns=["id", "nombre"])
    tipos_wcag = pd.DataFrame(qr.obtener_tipos_wcag())
    principios = pd.DataFrame(qr.obtener_principios())
    niveles = pd.DataFrame(qr.obtener_niveles())
    versiones = pd.DataFrame(qr.obtener_versiones())
    tipos_entidad = pd.DataFrame(qr.obtener_tipos_entidad())
    entidades = pd.DataFrame(qr.obtener_entidades_por_id(tipos_entidad.iloc[0,0]), columns=["id", "nombre", "id_tipo"])

    entidades_ids = list(entidades['id'])
    entidades_sql = f"({','.join(map(str, entidades_ids))})"

    principios_ids = list(principios['id'])
    principios_sql = f"({','.join(map(str, principios_ids))})"

    versiones_ids = list(versiones['id'])
    versiones_sql = f"({','.join(map(str, versiones_ids))})"

    niveles_ids = list(niveles['id'])
    niveles_sql = f"({','.join(map(str, niveles_ids))})"

    datos = pd.DataFrame(
        qr.obtener_datos(entidades_sql, principios_sql, versiones_sql, niveles_sql),
        columns=[
            "id_principio","principio","id_entidad","entidad",
            "id_criterio","criterio","id_descripcion","descripcion",
            "observaciones","version"
        ]
    )

    df_datos = pd.DataFrame({
        "Criterios": datos["criterio"],
        "Valores": datos["descripcion"],
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
        "niveles": niveles.to_dict('records')
    }