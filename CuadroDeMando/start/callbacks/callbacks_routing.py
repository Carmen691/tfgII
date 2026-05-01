from dash import Output, Input, State, callback_context, html, dcc
from dash.exceptions import PreventUpdate
from flask import session
import pandas as pd
import data.querys as qr


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


    @app.callback(
        Output("link-filtros", "children"),
        Output("link-cuadro", "children"),
        Output("link-datos", "children"),
        Output("link-importar", "children"),
        Output("admin-toggle", "children"),
        Output("link-usuarios", "children"),
        Output("link-auditorias", "children"),
        Output("logout-button", "children"),
        Input("store-idioma", "data")
    )
    def actualizar_textos_menu(idioma):
        return (
            qr.obtener_textos_interfaz(idioma, "menu", "filtros"),
            qr.obtener_textos_interfaz(idioma, "menu", "cuadro_mando"),
            qr.obtener_textos_interfaz(idioma, "menu", "tabla_datos"),
            qr.obtener_textos_interfaz(idioma, "menu", "importar_datos"),

            # admin-toggle tiene estructura HTML, no solo texto
            html.Div([
                html.Span(
                    qr.obtener_textos_interfaz(idioma, "menu", "panel_administracion"),
                    className="sidebar-admin-text"
                ),
                html.I(
                    className="bi bi-chevron-down sidebar-admin-icon",
                    style={"float": "right"}
                )
            ]),

            qr.obtener_textos_interfaz(idioma, "menu", "usuarios"),
            qr.obtener_textos_interfaz(idioma, "menu", "gestion_auditorias"),
            qr.obtener_textos_interfaz(idioma, "menu", "cerrar_sesion"),
        )