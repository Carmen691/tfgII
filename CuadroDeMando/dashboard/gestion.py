from dash import html, dcc
import data.querys as bd

def layout_gestion(idioma, auditorias):
    return html.Div([
    html.H2(bd.obtener_textos_interfaz(idioma, "gestion", "titulo")),

    html.Label(bd.obtener_textos_interfaz(idioma, "gestion", "auditorias")),
    dcc.Dropdown(
        id='auditorias-dropdown',
        options=[{'label': aud, 'value': aud} for aud in auditorias["nombre"].unique()],
        style={'width': '50%'}
    ),
    html.Br(),
    html.Button(bd.obtener_textos_interfaz(idioma, "usuarios", "eliminar"), id='borrar-auditoria-button', n_clicks=0),
    html.Div(id="mensaje-audtioria", style={"marginTop": "10px"})
    ])
