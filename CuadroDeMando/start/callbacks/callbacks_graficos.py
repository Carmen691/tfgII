import dash
from dash import Input, Output, State
from dash import html
import plotly.express as px
import pandas as pd
import data.querys as qr



def registrar_callbacks_graficos(app):

    @app.callback(
        Output('grafico-porcentaje', 'figure'),
        Output('grafico-principios', 'figure'),
        Input("store-data", "data"),
        prevent_initial_call=False
    )
    def actualizar_graficos(data):
        df = pd.DataFrame(data["df_datos"])

        fig = px.bar(
            df,
            x="Entidades",
            y="Valores",
            color="Criterios",
            barmode="stack"
        )

        porcentaje_cumplimiento = pd.DataFrame(qr.obtener_suma_cumplimiento(), columns = ["principio", "num_no_conseguido",
                                            "num_parcialmente_conseguido", "num_no_aplicable",
                                            "num_ampliamente_conseguido", "num_totalmente_conseguido"])
        df_porcentajes = pd.DataFrame({
            "Principio": porcentaje_cumplimiento["principio"],
            "No Conseguido": porcentaje_cumplimiento["num_no_conseguido"],
            "Parcialmente Conseguido": porcentaje_cumplimiento["num_parcialmente_conseguido"],
            "No Aplicable": porcentaje_cumplimiento["num_no_aplicable"],
            "Ampliamente Conseguido": porcentaje_cumplimiento["num_ampliamente_conseguido"],
            "Totalmente Conseguido": porcentaje_cumplimiento["num_totalmente_conseguido"]
        })

        df_melt = df_porcentajes.melt(
            id_vars=["Principio"],
            var_name="Estado",
            value_name="Valores"
        )

        fig2 = px.pie(
            df_melt,
            names="Estado",
            values="Valores",
            title="Cumplimiento de Principios"
        )


        return fig, fig2
    

    @app.callback(
        Output("cumplimiento-div", "children"),
        Input("store-data", "data"),
        Input("store-tipo-entidad", "data")
    )
    def actualizar_cumplimiento(data, tipoEntidad):
        datos_lista_principios = qr.obtener_cumplimiento_principios(tipoEntidad)

        datos_principios = {fila[0]: fila[1] for fila in datos_lista_principios}

        return [
            html.H4("% Cumplimiento"),
            html.P(f"Operable: {round(datos_principios.get('Operable', 0), 2)}%"),
            html.P(f"Comprensible: {round(datos_principios.get('Understandable', 0), 2)}%"),
            html.P(f"Robusto: {round(datos_principios.get('Robust', 0), 2)}%"),
            html.P(f"Perceptible: {round(datos_principios.get('Perceivable', 0), 2)}%"),
        ]
    

    @app.callback(
        Output("niveles-div", "children"),
        Input("store-data", "data"),
        Input("store-tipo-entidad", "data")
    )
    def actualizar_cumplimiento(data, tipoEntidad):
        datos_lista_niveles = qr.obtener_cumplimiento_niveles(tipoEntidad)

        datos_niveles =  {fila[0]: fila[1] for fila in datos_lista_niveles}

        return [
            html.H4("% Por niveles"),
            html.P(f"A: {round(datos_niveles.get('A', 0), 2)}%"),
            html.P(f"AA: {round(datos_niveles.get('AA', 0), 2)}%"),
            html.P(f"AAA: {round(datos_niveles.get('AAA', 0), 2)}%"),
        ]