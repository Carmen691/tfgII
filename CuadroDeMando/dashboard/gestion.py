from dash import html, dcc
import data.querys as bd

def layout_gestion():
    return html.Div([

        html.H2(id="titulo-gestion"),

        html.Label(id="label-auditorias"),

        dcc.Dropdown(
            id='auditorias-dropdown',
            style={'width': '50%'}
        ),

        html.Br(),

        html.Button(
            id='borrar-auditoria-button',
            n_clicks=0,
        ),

        html.Div(
            id="mensaje-auditoria",
            style={"marginTop": "10px"}
        )
    ])
