from dash import Output, Input, State, callback_context, html, dcc
import dash
from dash.exceptions import PreventUpdate
from flask import session
import pandas as pd
import data.querys as qr
from dash_iconify import DashIconify


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
        if 'user' not in session:
            return dcc.Location(pathname='/', id='redir-login')
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

        textos = qr.obtener_textos_seccion(idioma, "menu")

        def item(icono, texto):
            return [
                DashIconify(
                    icon=icono,
                    width=20,
                    className="sidebar-icon"
                ),
                html.Span(
                    texto,
                    className="menu-text"
                )
            ]

        return (
            item("tabler:filter", textos["filtros"]),
            item("tabler:chart-bar", textos["cuadro_mando"]),
            item("tabler:table", textos["tabla_datos"]),
            item("tabler:upload", textos["importar_datos"]),
            item("tabler:settings", textos["panel_administracion"]),
            item("tabler:users", textos["usuarios"]),
            item("tabler:file-description", textos["gestion_auditorias"]),
            item("tabler:logout", textos["cerrar_sesion"]),
        )


    @app.callback(
        Output('url', 'pathname'),
        Input('session-check', 'n_intervals')
    )
    def comprobar_sesion(n):
        if not session.get('user'):
            return '/login'

        return dash.no_update