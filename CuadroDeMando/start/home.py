import dash
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from dashboard.app import creardash
from data.querys import obtener_idioma, obtener_tipos_entidad, obtener_datos
from dashboard.layout import crear_layout



def crear_dash_app(flask_app): 
    idioma = pd.DataFrame(obtener_idioma(), columns=["id", "codigo", "nombre"])
    entidades = pd.DataFrame(obtener_tipos_entidad(), columns=["id", "nombre", "id_tipo"])
    datos = pd.DataFrame(obtener_datos(), columns = ["id_principio", "principio", "id_entidad", "entidad",
                                                        "id_criterio", "criterio", "descripcion", "observaciones",
                                                        "version"])

    # Datos de ejemplo
    df = pd.DataFrame({
        "Criterios": datos["criterio"],
        "Valores": datos["descripcion"],
        "Entidades": datos["entidad"],
    })

    df["Valores"] = df["Valores"].astype(str)
    df["Entidades"] = df["Entidades"].astype(str)

    fig = px.bar(df, x="Entidades", y="Valores", 
             title="Cumplimiento de WCAG por Entidad",
             labels={"value": "Numero de Criterios", "variable": "Estado"},
             color ="Criterios",
             barmode="stack",
             category_orders={"Entidades": df["Entidades"].unique().tolist()})  # Forzar el orden de las entidades
             

    external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css']
    app = Dash(__name__, server=flask_app, url_base_pathname='/dash/', suppress_callback_exceptions=True)


    layout_dashboard = crear_layout(df, idioma, entidades, fig)
    app.layout = layout_dashboard

    #app.layout = creardash(app, datos, df, idioma, entidades)


    # Callback para manejar la paginación
    @app.callback(
        dash.Output('tabla-datos', 'data'),
        dash.Output('tabla-datos', 'page_count'),  # Asegura que Dash detecta el total de páginas
        dash.Input('tabla-datos', 'page_current'),
        dash.Input('tabla-datos', 'page_size')
    )
    def actualizar_tabla(page_current, page_size):
        if page_current is None:
            page_current = 0
    
        start = page_current * page_size
        end = start + page_size
        data_paginada = df.iloc[start:end].to_dict('records')

        return data_paginada, (len(df) // page_size) + (1 if len(df) % page_size > 0 else 0)

    return app