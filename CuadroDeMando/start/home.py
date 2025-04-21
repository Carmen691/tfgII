from dashboard.filtros import layout_filtros
from dashboard.tablas import layout_datos
from dashboard.graficos import layout_graficos
import dash
from dash import Dash, dcc, html, dash_table
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


    @app.callback(
        dash.Output('page-content', 'children'),
        dash.Input('url', 'pathname')
    )
    def mostrar_contenido(pathname):
        if pathname == '/dash/' or pathname == '/dash':
            return layout_graficos(fig)
        elif pathname == '/dash/datos':
            return layout_datos(df)
        elif pathname == '/dash/filtros':
            return layout_filtros(idioma, entidades)
        else:
            return html.H2("Página no encontrada")
    
    @app.callback(
        dash.Output("sidebar", "style"),
        dash.Output("menu-content", "style"),
        dash.Output("main-content", "style"),  # <-- nuevo
        dash.Output("menu-collapsed", "data"),
        dash.Input("toggle-menu", "n_clicks"),
        dash.State("menu-collapsed", "data"),
    )
    def toggle_menu(n_clicks, is_collapsed):
        if n_clicks is None:
            raise dash.exceptions.PreventUpdate

        collapsed = not is_collapsed

        if collapsed:
            sidebar_style = {
                "position": "fixed", "top": "0", "left": "0",
                "width": "40px", "height": "100%",
                "backgroundColor": "#2c3e50", "paddingTop": "20px",
                "zIndex": "1000", "overflow": "hidden"
            }
            menu_content_style = {"display": "none"}
            content_style = {"marginLeft": "50px", "transition": "margin-left 0.3s ease", "padding": "20px"}
        else:
            sidebar_style = {
                "position": "fixed", "top": "0", "left": "0",
                "width": "250px", "height": "100%",
                "backgroundColor": "#2c3e50", "paddingTop": "20px",
                "zIndex": "1000", "overflow": "hidden"
            }
            menu_content_style = {"display": "block"}
            content_style = {"marginLeft": "260px", "transition": "margin-left 0.3s ease", "padding": "20px"}

        return sidebar_style, menu_content_style, content_style, collapsed

    @app.callback(
        dash. Output("toggle-menu", "children"),
        dash.Input("menu-collapsed", "data")
    )
    def update_arrow(collapsed):
        return "⮞" if collapsed else "⮜"
    
    return app