import dash
from dash import Input, Output, State, no_update
import plotly.express as px
import pandas as pd
from start.callbacks.services.data_services import cargar_datos, cargar_datos_inicio
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
            return cargar_datos_inicio(), True, False  
        return no_update, no_update, True
        

    @app.callback(
        Output('store-data', 'data'),
        Input('boton-actualizar', 'n_clicks'),
        State('tipo-entidad-dropdown', 'value'),
        State('entidad-dropdown', 'value'),
        State('principios-checklist', 'value'),
        State('wcag-version-checklist', 'value'),
        State('nivel-checklist', 'value'),
        prevent_initial_call=True
    )
    def actualizar_datos_filtros(n, tipo_entidad, entidades, principios, versiones, niveles):
        if n > 0:
            return cargar_datos(tipo_entidad, entidades, principios, versiones, niveles)
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
        dash.Output('tabla-datos', 'data'),
        dash.Input('url', 'pathname'),
        dash.State('store-data', 'data'),
    )
    def actualizar_tabla(path, data):

        if path != '/dash/datos':
            raise dash.exceptions.PreventUpdate

        return data
