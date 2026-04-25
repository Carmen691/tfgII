from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import data.querys as bd


def layout_filtros():
    return html.Div([
        html.Div(id="filtros-container")
    ])