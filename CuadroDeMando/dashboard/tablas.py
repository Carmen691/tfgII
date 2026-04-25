from dash import html
from dash import dash_table, dcc

from dash import html, dash_table, dcc
import pandas as pd

def layout_datos():
    return html.Div([
        html.Div(id="tabla-datos-container"),
        html.Button(
                id="btn-guardar-tabla",
                n_clicks=0
            ),
        html.Div(id="mensaje-guardar", style={"marginTop": "10px"})
    ])