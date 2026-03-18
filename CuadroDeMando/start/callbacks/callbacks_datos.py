import dash
from dash import Input, Output, State
import plotly.express as px
import pandas as pd


def registrar_callbacks_datos(app, data):

    df_datos = data["df_datos"]

    @app.callback(
        dash.Output('tabla-datos', 'data'),
        dash.Input('url', 'pathname'),
        dash.State('entidad-store', 'data'),
        dash.State('store-tipo-entidad', 'data'),
    )
    def actualizar_tabla(path, entidades, tipo_entidad):

        if path != '/dash/datos':
            raise dash.exceptions.PreventUpdate

        df = df_datos.copy()

        if entidades:
            df = df[df['Entidades'].isin(entidades)]

        return df.to_dict('records')
