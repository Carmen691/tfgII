from dash import Dash
import dash_bootstrap_components as dbc

from start.callbacks.callbacks_datos import registrar_callbacks_datos
from dashboard.layout import crear_layout
from start.callbacks.services.data_services import cargar_datos
from start.callbacks.callbacks_filtros import registrar_callbacks_filtros
from start.callbacks.callbacks_graficos import registrar_callbacks_graficos
from start.callbacks.callbacks_admin import registrar_callbacks_admin
from start.callbacks.callbacks_upload import registrar_callbacks_upload
from start.callbacks.callbacks_routing import registrar_callbacks_routing

def crear_dash_app(flask_app):

    app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/dash/',
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    app.layout = crear_layout()

    

    registrar_callbacks_datos(app)
    registrar_callbacks_routing(app)
    registrar_callbacks_admin(app)
    registrar_callbacks_filtros(app)
    registrar_callbacks_graficos(app)
    registrar_callbacks_upload(app)

    
    return app