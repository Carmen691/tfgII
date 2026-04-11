import dash
from dash import Input, Output, State
import plotly.express as px
import pandas as pd
from start.callbacks.services.data_services import cargar_datos
import data.querys as qr


from dash import ctx
from dash.exceptions import PreventUpdate

def registrar_callbacks_datos(app):
    @app.callback(
        Output('store-data', 'data', allow_duplicate=True),
        Input('init-done', 'data'),
        State('entidad-store', 'data'),
        State('store-tipo-entidad', 'data'),
        State('store-principios', 'data'),
        State('store-versiones', 'data'),
        State('store-niveles', 'data'),
        prevent_initial_call='initial_duplicate'
    )
    def actualizar_datos(cargar, entidad, tipo_entidad, principios, versiones, niveles):
        if cargar:
            return cargar_datos(tipo_entidad, entidad, principios, versiones, niveles)
    

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
        dash.State('entidad-store', 'data'),
        dash.State('store-tipo-entidad', 'data'),
        dash.State('store-data', 'data'),
        dash.State('store-principios', 'data'),
        dash.State('store-versiones', 'data'),
        dash.State('store-niveles', 'data'),
    )
    def actualizar_tabla(path, entidades, tipo_entidad, data, principios, versiones, niveles):

        if path != '/dash/datos':
            raise dash.exceptions.PreventUpdate

        df = data.copy()

        #if entidades:
        #    df = df[df['Entidades'].isin(entidades)]

        return df.to_dict('records')
