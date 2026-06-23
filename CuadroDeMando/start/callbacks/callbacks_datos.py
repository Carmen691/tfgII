import dash
from dash import Input, Output, State, no_update
from dash import html
from dash import dash_table
from flask import session
import plotly.express as px
import pandas as pd
from start.callbacks.services.data_services import cargar_datos, cargar_datos_inicio, cargar_tipo_entidades
import data.querys as qr


from dash import ctx
from dash.exceptions import PreventUpdate

def registrar_callbacks_datos(app):
    from dash import no_update

    @app.callback(
        Output('store-data', 'data', allow_duplicate=True),
        Output('init-done', 'data'),
        Output('init-trigger', 'disabled'),
        Input('init-trigger', 'n_intervals'),
        prevent_initial_call='initial_duplicate'
    )
    def actualizar_datos(cargar):
        if cargar < 2:
            datos = cargar_datos_inicio()
            return datos, True, False
        return no_update, no_update, True

    
    @app.callback(
        Output('tipo-entidad-dropdown', 'value', allow_duplicate=True),
        Input('store-data', 'data'),
        State('tipo-entidad-dropdown', 'value'),
        prevent_initial_call='initial_duplicate'
    )
    def actualizar_datos(datos, tipoEntidad):
        if tipoEntidad is None and datos is not None:
            return datos["tiposEntidad"][0]['id']
        return no_update
        

    @app.callback(
        Output('store-data', 'data', allow_duplicate=True),
        Input('boton-actualizar', 'n_clicks'),
        State('tipo-entidad-dropdown', 'value'),
        State('entidad-dropdown', 'value'),
        State('principios-checklist', 'value'),
        State('wcag-version-checklist', 'value'),
        State('nivel-checklist', 'value'),
        State('version-auditoria-dropdown', 'value'),
        prevent_initial_call='initial_duplicate'
    )
    def actualizar_datos_filtros(nact, tipo_entidad, entidades, principios, versiones, niveles, version_aud):
        if nact > 0:
            return cargar_datos(tipo_entidad, entidades, principios, versiones, niveles, version_aud)
        return no_update

    @app.callback(
        Output("tabla-datos-container", "children"),
        Input("store-data", "data"),
        Input("store-idioma", "data"),
    )
    def cargar_tabla_datos(data, idioma):

        if not data:
            return html.Div("Cargando datos...")

        df = pd.DataFrame(data["df_datos"])

        return dash_table.DataTable(
            id='tabla-datos',
            editable=True,
            page_action='native',
            page_current=0,
            page_size=10,
            data=df.to_dict('records'),
            columns=[
                {"name": qr.obtener_textos_interfaz(idioma, "tabla", "criterios"), "id": "Criterios"},
                {"name": qr.obtener_textos_interfaz(idioma, "tabla", "entidades"), "id": "Entidades"},
                {
                    "name": qr.obtener_textos_interfaz(idioma, "tabla", "valores"),
                    "id": "Valores",
                    "presentation": "dropdown",
                    "editable": True
                },
            ],
            hidden_columns=["ID"],
            dropdown_conditional=[
                {
                    "if": {"column_id": "Valores"},
                    "options": [
                        {
                            "label": row["descripcion"],
                            "value": row["id_descripcion"]
                        }
                        for _, row in pd.DataFrame(
                            qr.obtener_opciones_cumplimiento(idioma)
                        ).iterrows()
                    ],
                }
            ]
        )
    

    @app.callback(
        Output("btn-guardar-tabla", "children"),
        Input("store-idioma", "data")
    )
    def textos_gestion(idioma):

        return (
            qr.obtener_textos_interfaz(idioma, "auditorias", "guardar")
        )
    

    @app.callback(
        Output("tabla-actual-store", "data"),
        Input("tabla-datos", "data"),
        prevent_initial_call=True
    )
    def sincronizar_tabla_actual(data):
        return data

    
    @app.callback(
        Output("store-data", "data", allow_duplicate=True),
        Output("mensaje-guardar", "children"),
        Input("btn-guardar-tabla", "n_clicks"),
        State("store-data", "data"),
        State("tabla-actual-store", "data"),
        State("store-idioma", "data"),
        prevent_initial_call=True
    )
    def guardar_datos_tabla(n_clicks, data, datosn, idioma):
        if n_clicks > 0:

            datos_antiguos = pd.DataFrame(data["df_datos"])
            datos_nuevos = pd.DataFrame(datosn)

            df = datos_nuevos.merge(
                datos_antiguos,
                on="Id",
                suffixes=("_new", "_old")
            )

            cambios = df[df["Valores_new"] != df["Valores_old"]]

            if cambios.empty:
                return no_update, qr.obtener_textos_interfaz(idioma, "tabla", "guardar_vacio")
            
            tuplas_update = [
                (row["Valores_new"], row["Id"])
                for _, row in cambios.iterrows()
            ]

            result = qr.actualizar_datos_mediciones(tuplas_update)

            if result > 0:
                data["df_datos"]=datosn
                qr.registrar_auditoria(session.get('user'), 'GUARDAR_DATOS', 'Se han guardado los datos correctamente')
                return data, qr.obtener_textos_interfaz(idioma, "tabla", "guardar_ok")
            else:
                return no_update, qr.obtener_textos_interfaz(idioma, "tabla", "guardar_ko")
            return data
        return no_update