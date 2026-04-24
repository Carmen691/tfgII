import dash
from dash import Input, Output, State, no_update
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
        return no_update, no_update, True,

    
    @app.callback(
        Output('store-tipo-entidad', 'data', allow_duplicate=True),
        Input('store-data', 'data'),
        State('store-tipo-entidad', 'data'),
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
        Output('dropdown-sugerencias', 'options'),
        Input('store-data', 'data')
    )
    def actualizar_dropdown(data):
        if not data or "tiposEntidad" not in data:
            return []

        entidades = data["tiposEntidad"]

        if len(entidades) == 1 and isinstance(entidades[0], list):
            entidades = entidades[0]

        return [
            {"label": e["nombre"], "value": e["id"]}
            for e in entidades
        ]

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


    # @app.callback(
    #     dash.Output('tabla-datos', 'data'),
    #     dash.Input('url', 'pathname'),
    #     dash.State('store-data', 'data'),
    # )
    # def actualizar_tabla(path, data):

    #     if path != '/dash/datos':
    #         raise dash.exceptions.PreventUpdate

    #     return data
