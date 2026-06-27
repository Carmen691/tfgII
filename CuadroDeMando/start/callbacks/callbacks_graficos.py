import dash
from dash import Input, Output, State
from dash import html
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import data.querys as qr



def registrar_callbacks_graficos(app):

    @app.callback(
        Output("nombre_medicion", "children"),
        Output("version_medicion", "children"),
        Input("store-tipo-entidad", "data"),
        Input("store-idioma", "data")
    )
    def cargar_tabla_datos(data, idioma):
        nombre = qr.obtener_textos_interfaz(idioma, "menu", "cuadro_mando") + ": " + qr.obtener_tipos_entidad_por_id(data)[0][0]
        version = qr.obtener_textos_interfaz(idioma, "auditorias", "versionwcag") + ": " + qr.obtener_version_por_id_entidad(data)[0][0]

        return nombre, version




    @app.callback(
        Output('grafico-porcentaje', 'figure'),
        Output('grafico-principios', 'figure'),
        Output('grafico-niveles', 'figure'),
        Output("niveles-div", "children"),
        Output("datos-wcag-div", "children"),
        Output("cumplimiento-div", "children"),
        Input("url", "pathname"),
        State("store-entidad", "data"),
        State("store-principios", "data"),
        State("store-versiones", "data"),
        State("store-niveles", "data"),
        State("store-fecha", "data"),
        State("store-tipo-entidad", "data"),
        prevent_initial_call=False
    )
    def actualizar_graficos(pathname, entidades, principios, versiones, niveles, fecha, tipo_aud):
        if pathname != "/dash/cuadroMando":
            raise PreventUpdate
        
        if entidades:
            entidades_sql = f"({", ".join(map(str, entidades))})"
        else:
            entidades_sql = None
        if principios:
            principios_sql = f"({','.join(map(str, principios))})"
        else:
            principios_sql = None
        if versiones:
            versiones_sql = f"({", ".join(map(str, versiones))})"
        else:
            versiones_sql = None
        if niveles:
            niveles_sql = f"({", ".join(map(str, niveles))})"
        else:
            niveles_sql = None

        if not fecha:
            fecha = qr.obtener_versiones_auditoria(tipo_aud)[0][0]

        datos = pd.DataFrame(
        qr.obtener_datos(entidades_sql, principios_sql, versiones_sql, niveles_sql, fecha),
        columns=[
            "id_medicion","id_principio","principio","id_entidad","entidad",
            "id_criterio","criterio","id_descripcion","descripcion",
            "observaciones","version"
        ]
    )

        df_datos = pd.DataFrame({
            "Id":datos["id_medicion"],
            "Criterios": datos["criterio"],
            "Valores": datos["id_descripcion"],
            "Entidades": datos["entidad"],
        })

        df_datos["Entidades"] = df_datos["Entidades"].astype(str)
        df = df_datos.to_dict('records')

        porcentaje_cumplimiento = pd.DataFrame(qr.obtener_suma_cumplimiento(entidades_sql, principios_sql, versiones_sql, niveles_sql, fecha), 
                                            columns = ["principio", "num_no_conseguido",
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

        df_pct = df_melt.copy()
        df_pct["Total"] = df_pct.groupby("Principio")["Valores"].transform("sum")
        df_pct["Porcentaje"] = (df_pct["Valores"] / df_pct["Total"] * 100)

        orden_estados = [
            "No Conseguido",
            "Parcialmente Conseguido",
            "No Aplicable",
            "Ampliamente Conseguido",
            "Totalmente Conseguido"
        ]

        df_pct["Estado"] = pd.Categorical(
            df_pct["Estado"],
            categories=orden_estados,
            ordered=True
        )

        fig1 = px.bar(
            df_pct,
            x="Porcentaje",
            y="Principio",
            color="Estado",
            orientation="h",
            text="Porcentaje",
            title="Porcentaje por principios"
        )

        fig1.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='inside')

        fig1.update_layout(
            barmode="stack",
            xaxis_title="% de cumplimiento",
            yaxis_title="",
            legend_title="Estado",
            xaxis_range=[0, 100],
            height=450)
        

        datos_por_niveles = qr.obtener_cumplimiento_niveles(entidades_sql, principios_sql, versiones_sql, niveles_sql, fecha)
        df_niveles = pd.DataFrame(datos_por_niveles)

        orden_niveles = ["A", "AA", "AAA"]

        df_niveles["nombre"] = pd.Categorical(
            df_niveles["nombre"],
            categories=orden_niveles,
            ordered=True
        )

        df_niveles = df_niveles.sort_values("nombre")

        fig2 = px.bar(
            df_niveles,
            x="nombre",
            y="porcentaje",
            text="porcentaje",
            title="Porcentaje de cumplimiento por niveles WCAG"
        )

        # Mejoras visuales
        fig2.update_traces(
            texttemplate='%{text:.2f}%',
            textposition='outside'
        )

        fig2.update_layout(
            yaxis_title="% Cumplimiento",
            xaxis_title="Nivel WCAG",
            yaxis_range=[0, 100],
            height=400,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        df = pd.DataFrame(df)
        df_total = (
            df[df["Valores"] != 3]
            .groupby("Entidades")
            .size()
            .reset_index(name="Total")
        )

        df_ok = (
            df[df["Valores"].isin([4, 5])]
            .groupby("Entidades")
            .size()
            .reset_index(name="Cumplen")
        )

        df_entidades = df_total.merge(
            df_ok,
            on="Entidades",
            how="left"
        )

        df_entidades["Cumplen"] = df_entidades["Cumplen"].fillna(0)

        df_entidades["Porcentaje"] = (
            df_entidades["Cumplen"]
            / df_entidades["Total"]
            * 100
        )

        df_entidades = df_entidades.sort_values(
            "Porcentaje",
            ascending=True
        )

        fig3 = px.bar(
            df_entidades,
            x="Porcentaje",
            y="Entidades",
            orientation="h",
            text="Porcentaje",
            title="Porcentaje de cumplimiento por entidad"
        )

        fig3.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside'
        )

        fig3.update_layout(
            xaxis_title="% Cumplimiento",
            yaxis_title="",
            xaxis_range=[0, 100],
            height=450
        )

        datos_niveles =  {fila[0]: fila[1] for fila in datos_por_niveles}

        est = [
            html.H4("% Por niveles"),
            html.P(f"A: {round(datos_niveles.get('A', 0), 2)}%"),
            html.P(f"AA: {round(datos_niveles.get('AA', 0), 2)}%"),
            html.P(f"AAA: {round(datos_niveles.get('AAA', 0), 2)}%"),
        ]

        datos_wcag = html.Div([
            html.H4("DATOS WCAG"),
            html.P(f"Total Entidades: {qr.obtener_numero_entidades(entidades_sql)}"),
            html.P(f"Total Mediciones: {qr.obtener_numero_mediciones(entidades_sql)}"),
            html.P(f"Cumplimientos: {qr.obtener_numero_cumplimientos(entidades_sql)}"),
            html.P(
                f"Porcentaje Cumplimiento: "
                f"{qr.obtener_porcentaje_cumplimiento(entidades_sql)} %"
            )
        ])

        datos_lista_principios = qr.obtener_cumplimiento_principios(entidades_sql, principios_sql, versiones_sql, niveles_sql, fecha)

        datos_principios = {fila[0]: fila[1] for fila in datos_lista_principios}

        cumplimiento = [
            html.H4("% Cumplimiento"),
            html.P(f"Operable: {round(datos_principios.get('Operable', 0), 2)}%"),
            html.P(f"Comprensible: {round(datos_principios.get('Understandable', 0), 2)}%"),
            html.P(f"Robusto: {round(datos_principios.get('Robust', 0), 2)}%"),
            html.P(f"Perceptible: {round(datos_principios.get('Perceivable', 0), 2)}%"),
        ]

        return fig1, fig2, fig3, est, datos_wcag, cumplimiento
    