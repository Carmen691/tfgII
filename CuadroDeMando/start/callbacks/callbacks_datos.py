import dash
from dash import Input, Output, State, no_update
from dash import html
from dash import dash_table
from flask import session
import plotly.express as px
import pandas as pd
import data.querys as qr


from dash import ctx
from dash.exceptions import PreventUpdate

def registrar_callbacks_datos(app):
    from dash import no_update
    
    @app.callback(
        Output('tipo-entidad-dropdown', 'value', allow_duplicate=True),
        Input('store-tipo-entidad', 'data'),
        State('tipo-entidad-dropdown', 'value'),
        prevent_initial_call='initial_duplicate'
    )
    def actualizar_datos(data, tipoEntidad):
        tipos = pd.DataFrame(qr.obtener_tipos_entidad()).to_dict('records')
        if tipoEntidad is None:
            return tipos[0]['id']
        return no_update
        
    @app.callback(
        Output("tabla-datos", "data"),
        Output("tabla-datos", "columns"),
        Output("tabla-datos", "dropdown_conditional"),
        Input("url", "pathname"),
        Input("store-idioma", "data"),
        State("store-entidad", "data"),
        State("store-principios", "data"),
        State("store-versiones", "data"),
        State("store-niveles", "data"),
        State("store-fecha", "data"),
        State("store-tipo-entidad", "data")
    )
    def cargar_tabla_datos(
        pathname,
        idioma,
        entidades_sql,
        principios_sql,
        versiones_sql,
        niveles_sql,
        version_aud,
        tipo_aud
    ):

        if pathname != "/dash/datos":
            raise PreventUpdate

        textos = qr.obtener_textos_seccion(idioma, "tabla")

        ent_sel = (
            None
            if not entidades_sql
            else "(" + ",".join(map(str, entidades_sql)) + ")"
        )

        princ_sel = (
            None
            if not principios_sql
            else "(" + ",".join(map(str, principios_sql)) + ")"
        )

        ver_sel = (
            None
            if not versiones_sql
            else "(" + ",".join(map(str, versiones_sql)) + ")"
        )

        niv_sel = (
            None
            if not niveles_sql
            else "(" + ",".join(map(str, niveles_sql)) + ")"
        )

        if not version_aud:
            version_aud = qr.obtener_versiones_auditoria(tipo_aud)[0][0]

        id_escala = qr.obtener_escala_tipo_auditoria(tipo_aud)[0][0]

        datos = pd.DataFrame(
            qr.obtener_datos(
                ent_sel,
                princ_sel,
                ver_sel,
                niv_sel,
                version_aud
            ),
            columns=[
                "id_medicion",
                "id_principio",
                "principio",
                "id_entidad",
                "entidad",
                "id_criterio",
                "criterio",
                "id_descripcion",
                "descripcion",
                "observaciones",
                "version",
            ],
        )

        df = pd.DataFrame(
            {
                "Id": datos["id_medicion"],
                "Criterios": datos["criterio"],
                "Valores": datos["id_descripcion"],
                "Estado": datos["descripcion"],
                "Entidades": datos["entidad"].astype(str),
            }
        ).to_dict("records")

        columnas = [
            {
                "name": textos["criterios"],
                "id": "Criterios",
            },
            {
                "name": textos["entidades"],
                "id": "Entidades",
            },
            {
                "name": textos["valores"],
                "id": "Valores",
                "presentation": "dropdown",
                "editable": True,
            },
        ]

        opciones = qr.obtener_opciones_cumplimiento(
            idioma,
            id_escala
        )

        dropdown = [
            {
                "if": {"column_id": "Valores"},
                "options": [
                    {
                        "label": descripcion,
                        "value": id_descripcion,
                    }
                    for id_descripcion, descripcion in opciones
                ],
            }
        ]

        return df, columnas, dropdown

    @app.callback(
        Output("btn-guardar-tabla", "children"),
        Input("store-idioma", "data")
    )
    def textos_gestion(idioma):

        textos = qr.obtener_textos_seccion(idioma, "auditorias")

        return textos["guardar"]
    

    @app.callback(
        Output("tabla-actual-store", "data"),
        Input("tabla-datos", "data"),
        prevent_initial_call=True
    )
    def sincronizar_tabla_actual(data):
        return data

    
    @app.callback(
        Output("mensaje-guardar", "children"),
        Output("btn-guardar-tabla", "disabled"),
        Input("btn-guardar-tabla", "n_clicks"),
        State("tabla-actual-store", "data"),
        State("store-idioma", "data"),
        State("store-entidad", "data"),
        State("store-principios", "data"),
        State("store-versiones", "data"),
        State("store-niveles", "data"),
        State("store-fecha", "data"),
        State("store-tipo-entidad", "data"),
        prevent_initial_call=True
    )
    def guardar_datos_tabla(
        n_clicks,
        datosn,
        idioma,
        entidades_sql,
        principios_sql,
        versiones_sql,
        niveles_sql,
        version_aud,
        tipo_aud
    ):

        if n_clicks <= 0:
            return no_update

        textos = qr.obtener_textos_seccion(idioma, "tabla")

        ent_sel = (
            None
            if not entidades_sql
            else "(" + ",".join(map(str, entidades_sql)) + ")"
        )

        princ_sel = (
            None
            if not principios_sql
            else "(" + ",".join(map(str, principios_sql)) + ")"
        )

        ver_sel = (
            None
            if not versiones_sql
            else "(" + ",".join(map(str, versiones_sql)) + ")"
        )

        niv_sel = (
            None
            if not niveles_sql
            else "(" + ",".join(map(str, niveles_sql)) + ")"
        )

        if not version_aud:
            version_aud = qr.obtener_versiones_auditoria(tipo_aud)[0][0]

        datos = pd.DataFrame(
            qr.obtener_datos(
                ent_sel,
                princ_sel,
                ver_sel,
                niv_sel,
                version_aud
            ),
            columns=[
                "id_medicion",
                "id_principio",
                "principio",
                "id_entidad",
                "entidad",
                "id_criterio",
                "criterio",
                "id_descripcion",
                "descripcion",
                "observaciones",
                "version"
            ]
        )

        datos_antiguos = pd.DataFrame({
            "Id": datos["id_medicion"],
            "Criterios": datos["criterio"],
            "Valores": datos["id_descripcion"],
            "Entidades": datos["entidad"].astype(str),
        })

        datos_nuevos = pd.DataFrame(datosn)

        df = datos_nuevos.merge(
            datos_antiguos,
            on="Id",
            suffixes=("_new", "_old")
        )

        cambios = df[
            df["Valores_new"] != df["Valores_old"]
        ]

        if cambios.empty:
            return no_update, textos["guardar_vacio"]

        tuplas_update = [
            (
                row["Valores_new"],
                row["Id"]
            )
            for _, row in cambios.iterrows()
        ]

        result = qr.actualizar_datos_mediciones(
            tuplas_update
        )

        if result > 0:

            qr.registrar_auditoria(
                session.get("user"),
                "GUARDAR_DATOS",
                "Se han guardado los datos correctamente"
            )

            return (
                textos["guardar_ok"],
                True
            )

        return (
            textos["guardar_ko"],
            False
        )

    @app.callback(
        Output("btn-guardar-tabla", "disabled"),
        Input("tabla-datos", "data_timestamp"),
        prevent_initial_call=True,
    )
    def activar_guardado(_):
        return False