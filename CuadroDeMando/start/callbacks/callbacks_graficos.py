import dash
from dash import Input, Output, State
import plotly.express as px
import pandas as pd


def registrar_callbacks_graficos(app, data):

    df_datos = data["df_datos"]

    @app.callback(
        Output('grafico-porcentaje', 'figure'),
        Input('url', 'pathname'),
        State('entidad-store', 'data'),
        State('store-tipo-entidad', 'data'),
        prevent_initial_call=False
    )
    def actualizar_graficos(pathname, entidades, tipo_entidad):

        if pathname != "/dash/cuadroMando":
            raise dash.exceptions.PreventUpdate

        df = df_datos.copy()

        if entidades:
            df = df[df['Entidades'].isin(entidades)]

        fig = px.bar(
            df,
            x="Entidades",
            y="Valores",
            color="Criterios",
            barmode="stack"
        )

        return fig