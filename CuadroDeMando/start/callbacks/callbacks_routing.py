from dash import Output, Input, State, callback_context, html, dcc
from dash.exceptions import PreventUpdate
from flask import session
import pandas as pd

from start.callbacks.services.data_services import cargar_datos
from dashboard.filtros import layout_filtros
from dashboard.tablas import layout_datos
from dashboard.graficos import layout_graficos
from dashboard.usuarios import layout_usuarios
from dashboard.gestion import layout_gestion
from dashboard.importar import layout_importar


def registrar_callbacks_routing(app):
    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')

    )
    def mostrar_contenido(pathname):
        if pathname == '/dash/':
            return dcc.Location(href='/dash/filtros', id='redir')


        elif pathname == '/dash/cuadroMando':
            return layout_graficos()

        elif pathname == '/dash/datos':
            return layout_datos()

        elif pathname == '/dash/filtros':
            return layout_filtros()

        elif pathname == '/dash/administracion/usuarios':
            return layout_usuarios()

        elif pathname == '/dash/administracion/auditorias':
            return layout_gestion()

        elif pathname == '/dash/importar':
            return layout_importar()

        return html.H2("Página no encontrada")
    

    @app.callback(
        Output("store-idioma", "data"),
        Input("idioma-dropdown", "value")
    )
    def cambiar_idioma(idioma):
        return idioma

    # @app.callback(
    #     Output("store-data", "data"),
    #     Output("store-tipo-entidad", "data"),
    #     Output("store-principios", "data"),
    #     Output("store-versiones", "data"),
    #     Output("store-niveles", "data"),
    #     Output("store-entidad", "data"),
    #     Output("init-done", "data"),
    #     Output("url", "pathname"),
    #     Input("logout-button", "n_clicks"),
    #     prevent_initial_call=True
    # )
    # def logout(n):

    #     if not n:
    #         raise PreventUpdate

    #     # aquí si además quieres limpiar sesión Flask:
    #     session.clear()

    #     return (
    #         None,
    #         None,
    #         None,
    #         None,
    #         None,
    #         None,
    #         None,
    #         "/login"
    #     )


