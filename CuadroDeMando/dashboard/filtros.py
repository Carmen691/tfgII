from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import data.querys as bd

def layout_filtros():
    return dcc.Loading(
        id="loading-filtros",
        type="circle",
        fullscreen=False,
        children=html.Div([

            html.Div([

                # 🔹 FILTROS
                html.Div(id="filtros-container"),


            ], className="dashboard-card filtros-wrapper")

        ])
    )