from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import data.querys as bd


def layout_filtros():
    return dcc.Loading(
        id="loading-filtros",
        type="circle",  # "default", "circle", "dot", "cube"
        fullscreen=False,
        children=html.Div([
            html.Div(
                id="filtros-container",
                className="dashboard-card"
            )
        ])
    )