import dash
from dash import Input, Output, State
from dash import html
import plotly.express as px
import pandas as pd
import data.querys as qr



def registrar_callbacks_graficos(app):

    @app.callback(
        Output('grafico-porcentaje', 'figure'),
        Input('url', 'pathname'),
        State('entidad-store', 'data'),
        State('store-tipo-entidad', 'data'),
        State('store-data', 'data'),
        prevent_initial_call=False
    )
    def actualizar_graficos(pathname, entidades, tipo_entidad, data):

        if pathname != "/dash/cuadroMando":
            raise dash.exceptions.PreventUpdate

        df = pd.DataFrame(data["df_datos"])

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
    

    @app.callback(
        Output("cumplimiento-div", "children"),
        Input("store-data", "data")
    )
    def actualizar_cumplimiento(tipoEntidad):
        datos_lista = qr.obtener_cumplimiento_principios(tipoEntidad)
        datos = {fila[0]: fila[1] for fila in datos_lista}

        return [
            html.H4("% Cumplimiento"),
            html.P(f"Operable: {round(datos.get('Operable', 0), 2)}%"),
            html.P(f"Comprensible: {round(datos.get('Understandable', 0), 2)}%"),
            html.P(f"Robusto: {round(datos.get('Robust', 0), 2)}%"),
            html.P(f"Perceptible: {round(datos.get('Perceivable', 0), 2)}%"),
        ]