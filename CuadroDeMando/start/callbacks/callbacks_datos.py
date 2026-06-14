import dash
from dash import Input, Output, State, no_update
from dash import html
from dash import dash_table
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
        prevent_initial_call='initial_duplicate'
    )
    def actualizar_datos_filtros(nact, tipo_entidad, entidades, principios, versiones, niveles):
        if nact > 0:
            return cargar_datos(tipo_entidad, entidades, principios, versiones, niveles)
        return no_update


    @app.callback(
        Output('store-data', 'data'),
        Input('add-option-button', 'n_clicks'),
        State('store-data', 'data'),
        prevent_initial_call=True
    )
    def actualizar_datos_filtros(nent, store_data):
        if nent > 0:
            store_data["tiposEntidad"] = cargar_tipo_entidades()
            return store_data
        return no_update
    

    @app.callback(
        dash.Output('mensaje-confirmacion', 'children'),
        dash.Output('refresh-trigger', 'data'),
        dash.Input('add-option-button', 'n_clicks'),
        dash.State('input-texto', 'value'),
        prevent_initial_call=True
    )
    def guardar_texto(n_clicks, valor_input):
        if not valor_input:
            return 'No hay texto para guardar', dash.no_update

        mensaje = qr.guardar_nuevo_tipo_entidad(valor_input)

        if mensaje == 0:
            return '❌ Error al guardar el nuevo tipo', dash.no_update
        else:
            return '✅ Tipo guardado correctamente', {'refresh': True}


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
                {"name": "Criterios", "id": "Criterios"},
                {"name": "Entidades", "id": "Entidades"},
                {
                    "name": "Valores",
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
                            "value": row["id_escala"]
                        }
                        for _, row in pd.DataFrame(
                            qr.obtener_opciones_cumplimiento()
                        ).iterrows()
                    ],
                }
            ],
             css=[
                {
                    "selector": ".dash-dropdown",
                    "rule": "position: relative !important; z-index: 9999 !important;"
                },
                {
                    "selector": ".Select-menu-outer",
                    "rule": "display: block !important; z-index: 10000 !important;"
                },
                {
                    "selector": ".show-hide",
                    "rule": "display: none"
                },
                {
                    "selector": ".previous-next-container input",
                    "rule": """
                        width: 30px !important;
                        height: 30px !important;
                        min-width: 30px !important;
                        max-width: 30px !important;

                        padding: 0 !important;
                        margin: 0 4px !important;
                        line-height: 30px !important;
                        text-align: center !important;

                        border: 1px solid #d1d5db !important;
                        border-radius: 8px !important;

                        font-size: 14px !important;
                        font-weight: 500 !important;

                        background: white !important;
                        box-sizing: border-box !important;
                    """
                },
                {
                    "selector": ".previous-next-container input[type=number]",
                    "rule": """
                        appearance: textfield !important;
                        -moz-appearance: textfield !important;
                        -webkit-appearance: none !important;
                    """
                },
                {
                    "selector": ".previous-next-container button",
                    "rule": """
                        width: 36px !important;
                        height: 36px !important;
                        min-width: 36px !important;
                            min-height: 36px !important;

                            padding: 0 !important;
                            margin: 0 2px !important;

                            border-radius: 8px !important;
                            font-weight: 600 !important;
                        """
                    },
                {
                    "selector": ".previous-next-container button",
                    "rule": """
                        border-radius: 8px !important;
                        font-weight: 600 !important;
                    """
                }
            ],
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
        prevent_initial_call=True
    )
    def guardar_datos_tabla(n_clicks, data, datosn):
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
                return no_update, "No hay cambios que guardar"
            
            tuplas_update = [
                (row["Valores_new"], row["Id"])
                for _, row in cambios.iterrows()
            ]

            result = qr.actualizar_datos_mediciones(tuplas_update)

            if result > 0:
                data["df_datos"]=datosn
                return data, "Se ha guardado correctamente"
            else:
                return no_update, "No se ha realizado el guardado"
            return data
        return no_update