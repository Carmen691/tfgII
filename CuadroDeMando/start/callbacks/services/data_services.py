import pandas as pd
import data.querys as qr


def cargar_datos(tipo_entidad=None, entidades=None, principios=None, versiones=None, niveles=None):
    idioma = pd.DataFrame(qr.obtener_idioma(), columns=["id", "codigo", "nombre"])
    entidades = pd.DataFrame(qr.obtener_entidades(), columns=["id", "nombre", "id_tipo"])
    usuarios = pd.DataFrame(qr.obtener_usuarios(), columns=["id", "usuario"])
    auditorias = pd.DataFrame(qr.obtener_auditorias(), columns=["id", "nombre"])
    tipos_entidad = pd.DataFrame(qr.obtener_tipos_entidad())
    tipos_wcag = pd.DataFrame(qr.obtener_tipos_wcag())
    principios = pd.DataFrame(qr.obtener_principios())
    niveles = pd.DataFrame(qr.obtener_niveles())

    datos = pd.DataFrame(
        qr.obtener_datos(tipo_entidad, entidades, principios, versiones, niveles),
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