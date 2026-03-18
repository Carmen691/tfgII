import pandas as pd
import data.querys as qr


def cargar_datos():

    idioma = pd.DataFrame(qr.obtener_idioma(), columns=["id", "codigo", "nombre"])
    entidades = pd.DataFrame(qr.obtener_entidades(), columns=["id", "nombre", "id_tipo"])
    usuarios = pd.DataFrame(qr.obtener_usuarios(), columns=["id", "usuario"])
    auditorias = pd.DataFrame(qr.obtener_auditorias(), columns=["id", "nombre"])
    tipos_entidad = pd.DataFrame(qr.obtener_tipos_entidad())
    tipos_wcag = pd.DataFrame(qr.obtener_tipos_wcag())

    datos = pd.DataFrame(
        qr.obtener_datos(),
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
        "idioma": idioma,
        "entidades": entidades,
        "usuarios": usuarios,
        "auditorias": auditorias,
        "datos": datos,
        "df_datos": df_datos,
        "tiposEntidad": tipos_entidad,
        "tiposWCAG": tipos_wcag
    }