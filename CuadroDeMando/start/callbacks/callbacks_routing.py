from dash import Output, Input, State, html, dcc
from dash.exceptions import PreventUpdate
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
        Input('store-idioma', 'data'),
        Input('url', 'pathname'),
        Input('store-data', 'data'),
        State('store-tipo-entidad', 'data'),

    )
    def mostrar_contenido(idioma_sel, pathname, data, tipoEntidad):
        if not data:
            raise PreventUpdate
        entidades = pd.DataFrame(data["entidades"])
        usuarios = pd.DataFrame(data["usuarios"])
        auditorias = pd.DataFrame(data["auditorias"])
        df_datos = pd.DataFrame(data["df_datos"])

        tiposEntidad = data["tiposEntidad"]
        tiposWCAG = pd.DataFrame(data["tiposWCAG"])
        principios = pd.DataFrame(data["principios"])
        niveles = pd.DataFrame(data["niveles"])

        if len(tiposEntidad) == 1 and isinstance(tiposEntidad[0], list):
            tiposEntidad = tiposEntidad[0]

        if pathname == '/dash/':
            return dcc.Location(href='/dash/filtros', id='redir')

        elif pathname == '/dash/cuadroMando':
            return layout_graficos(idioma_sel, None, None, None, tipoEntidad)

        elif pathname == '/dash/datos':
            return layout_datos(idioma_sel, df_datos)

        elif pathname == '/dash/filtros':
            return layout_filtros(idioma_sel, tiposEntidad, entidades, tiposWCAG, principios, niveles)

        elif pathname == '/dash/administracion/usuarios':
            return layout_usuarios(idioma_sel, usuarios)

        elif pathname == '/dash/administracion/auditorias':
            return layout_gestion(idioma_sel, auditorias)

        elif pathname == '/dash/importar':
            return layout_importar(idioma_sel, tiposEntidad, tiposWCAG)

        return html.H2("Página no encontrada")