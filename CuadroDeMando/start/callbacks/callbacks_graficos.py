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

        menu = qr.obtener_textos_seccion(idioma, "menu")
        auditorias = qr.obtener_textos_seccion(idioma, "auditorias")

        nombre = (
            menu["cuadro_mando"]
            + ": "
            + qr.obtener_tipos_entidad_por_id(data)[0][0]
        )

        version = (
            auditorias["versionwcag"]
            + ": "
            + qr.obtener_version_por_id_entidad(data)[0][0]
        )

        return nombre, version



    @app.callback(
        Output('grafico-porcentaje', 'figure'),
        Output('grafico-principios', 'figure'),
        Output('grafico-niveles', 'figure'),
        Output("niveles-div", "children"),
        Output("datos-wcag-div", "children"),
        Output("cumplimiento-div", "children"),
        Output("grafico-heat", "figure"),
        Output("grafico-problematicos", "figure"),
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
            "Estado": datos["descripcion"],
            "Principios": datos["principio"],
        })

        df_datos["Entidades"] = df_datos["Entidades"].astype(str)

        suma_cumplimiento, columnas = qr.obtener_suma_cumplimiento(entidades_sql, principios_sql, versiones_sql, niveles_sql, fecha)
        porcentaje_cumplimiento = pd.DataFrame(suma_cumplimiento, 
                                            columns = columnas)
        renombrar = {
            "principio": "Principio",
            "no_conseguido": "No Conseguido",
            "parcialmente_conseguido": "Parcialmente Conseguido",
            "no_aplicable": "No Aplicable",
            "ampliamente_conseguido": "Ampliamente Conseguido",
            "totalmente_conseguido": "Totalmente Conseguido"
        }

        df_porcentajes = porcentaje_cumplimiento.rename(columns=renombrar)

        df_melt = df_porcentajes.melt(
            id_vars=["Principio"],
            var_name="Estado",
            value_name="Valores"
        )

        df_pct = df_melt.copy()
        df_pct["Total"] = df_pct.groupby("Principio")["Valores"].transform("sum")
        df_pct["Porcentaje"] = (df_pct["Valores"] / df_pct["Total"] * 100)

        orden_estados = [col for col in df_porcentajes.columns if col != "Principio"]

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

        df_ent = pd.DataFrame(df_datos)


        # -------- datasets ----------
        df_top = preparar_df(df_ent, "top", 10)
        df_bottom = preparar_df(df_ent, "bottom", 10)
        df_all = preparar_df(df_ent, "all", 9999)


        # -------- figura ----------
        fig3 = px.bar(
            df_top,
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
            yaxis=dict(autorange="reversed"),
            updatemenus=[
                dict(
                    type="dropdown",
                    direction="down",
                    showactive=True,
                    x=1.15,          # derecha del gráfico
                    y=1,             # arriba
                    xanchor="left",
                    yanchor="top",
                    buttons=[
                        dict(
                            label="Top 10",
                            method="update",
                            args=[
                                {
                                    "x": [df_top["Porcentaje"]],
                                    "y": [df_top["Entidades"]],
                                    "text": [df_top["Porcentaje"]]
                                },
                                {
                                    "height": min(max(450, len(df_top) * 22), 900)
                                }
                            ]
                        ),
                        dict(
                            label="Bottom 10",
                            method="update",
                            args=[
                                {
                                    "x": [df_bottom["Porcentaje"]],
                                    "y": [df_bottom["Entidades"]],
                                    "text": [df_bottom["Porcentaje"]]
                                },
                                {
                                    "height": min(max(450, len(df_bottom) * 22), 900)
                                }
                            ]
                        ),
                        dict(
                            label="Todos",
                            method="update",
                            args=[
                                {
                                    "x": [df_all["Porcentaje"]],
                                    "y": [df_all["Entidades"]],
                                    "text": [df_all["Porcentaje"]]
                                },
                                {
                                    "height": min(max(450, len(df_all) * 22), 900)
                                }
                            ]
                        )
                    ]
                )
            ]
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


        df_heat = pd.DataFrame(df_datos)
        df_heat_top = preparar_heatmap(df_heat, "top", 10)
        df_heat_bottom = preparar_heatmap(df_heat, "bottom", 10)
        df_heat_all = preparar_heatmap(df_heat, "all")

        fig_heat = px.density_heatmap(
            df_heat_all,
            x="Principios",
            y="Entidades",
            z="Porcentaje",
            color_continuous_scale="Blues",
            title="Heatmap de cumplimiento (Entidad vs Principio)"
        )

        fig_heat.update_layout(
            height=600,

            updatemenus=[
                dict(
                    type="dropdown",
                    direction="down",
                    showactive=True,
                    x=1.15,
                    y=1,
                    xanchor="left",
                    yanchor="top",

                    buttons=[
                        dict(
                            label="Top 10",
                            method="update",
                            args=[
                                {
                                    "x": [df_heat_top["Criterios"]],
                                    "y": [df_heat_top["Entidades"]],
                                    "z": [df_heat_top["Porcentaje"]]
                                }
                            ]
                        ),

                        dict(
                            label="Bottom 10",
                            method="update",
                            args=[
                                {
                                    "x": [df_heat_bottom["Criterios"]],
                                    "y": [df_heat_bottom["Entidades"]],
                                    "z": [df_heat_bottom["Porcentaje"]]
                                }
                            ]
                        ),

                        dict(
                            label="Todos",
                            method="update",
                            args=[
                                {
                                    "x": [df_heat_all["Criterios"]],
                                    "y": [df_heat_all["Entidades"]],
                                    "z": [df_heat_all["Porcentaje"]]
                                }
                            ]
                        )
                    ]
                )
            ]
        )

       # Fig 4

        df_estados = (
            df_datos.groupby("Estado")
            .size()
            .reset_index(name="Cantidad")
        )
        
        df_estados["Porcentaje"] = (
            df_estados["Cantidad"] /
            df_estados["Cantidad"].sum()
            * 100
        )

        fig4 = px.bar(
            df_estados,
            x="Porcentaje",
            y="Estado",
            orientation="h",
            text="Porcentaje",
            color="Estado",
            title="Distribución de estados"
        )

        fig4.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        fig4.update_layout(
            showlegend=False,
            xaxis_range=[0, 100],
            xaxis_title="% del total",
            yaxis_title="",
            height=400
        )

        return fig1, fig2, fig3, est, datos_wcag, cumplimiento, fig_heat, fig4
    
    
def preparar_df(df, modo, n=10):

    df_total = (
        df[df["Estado"] != "No aplicable"]
        .groupby("Entidades")
        .size()
        .reset_index(name="Total")
    )

    estados_cumplen = ["Ampliamente conseguido", "Totalmente conseguido"]

    df_ok = (
        df[df["Estado"].isin(estados_cumplen)]
        .groupby("Entidades")
        .size()
        .reset_index(name="Cumplen")
    )

    df_entidades = df_total.merge(df_ok, on="Entidades", how="left")
    df_entidades["Cumplen"] = df_entidades["Cumplen"].fillna(0)

    df_entidades["Porcentaje"] = (
        df_entidades["Cumplen"] / df_entidades["Total"] * 100
    )

    if modo == "top":
        df_entidades = df_entidades.sort_values("Porcentaje", ascending=False).head(n)

    elif modo == "bottom":
        df_entidades = df_entidades.sort_values("Porcentaje", ascending=True).head(n)

    return df_entidades


def preparar_heatmap(df, modo="top", n=10):

    estados_cumplen = [
        "Ampliamente conseguido",
        "Totalmente conseguido"
    ]

    df["Cumple"] = (
        df["Estado"]
        .isin(estados_cumplen)
        .astype(int)
    )

    # porcentaje de cumplimiento por entidad y criterio
    df = (
        df
        .groupby(["Entidades", "Principios", "Criterios"])["Cumple"]
        .mean()
        .reset_index()
    )

    df["Porcentaje"] = df["Cumple"] * 100

    if modo == "top":
        entidades = (
            df.groupby("Entidades")["Porcentaje"]
            .mean()
            .sort_values(ascending=False)
            .head(n)
            .index
        )

    elif modo == "bottom":
        entidades = (
            df.groupby("Entidades")["Porcentaje"]
            .mean()
            .sort_values(ascending=True)
            .head(n)
            .index
        )

    else:
        entidades = df["Entidades"].unique()

    return df[df["Entidades"].isin(entidades)]
