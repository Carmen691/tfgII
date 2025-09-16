from dash import html, dcc
import dash_bootstrap_components as dbc
import data.querys as bd

def layout_usuarios(idioma, usuarios):
    return html.Div([
        html.H2(bd.obtener_textos_interfaz(idioma, "usuarios", "eliminar_usuarios")),

        html.Div([
            html.Label(bd.obtener_textos_interfaz(idioma, "usuarios", "usuarios"), style={'marginRight': '10px', 'alignSelf': 'center'}),
            dcc.Dropdown(
                id='usuarios-dropdown',
                placeholder=bd.obtener_textos_interfaz(idioma, "usuarios", "seleccionar"),
                options=[{'label': usu, 'value': usu} for usu in usuarios["usuario"].unique()],
                style={'width': '300px', 'marginRight': '10px'}
            ),
            html.Button(bd.obtener_textos_interfaz(idioma, "usuarios", "eliminar"), id='borrar-usuario-button', n_clicks=0),
            dbc.Modal([
                dbc.ModalHeader(bd.obtener_textos_interfaz(idioma, "usuarios", "confirmacion")),
                dbc.ModalBody(bd.obtener_textos_interfaz(idioma, "usuarios", "msg_confirmacion")),
                dbc.ModalFooter([
                    dbc.Button(bd.obtener_textos_interfaz(idioma, "usuarios", "cancelar"), id="cancelar-eliminar", className="ms-auto", n_clicks=0),
                    dbc.Button(bd.obtener_textos_interfaz(idioma, "usuarios", "eliminar"), id="confirmar-eliminar", color="danger", n_clicks=0),
                ])
            ], id="modal-confirmacion", is_open=False),
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '15px'}),

        html.H2(bd.obtener_textos_interfaz(idioma, "usuarios", "anadir_usuarios")),
        html.Div([
        dcc.Input(
            id='input-usuario',
            type='text',
            placeholder=bd.obtener_textos_interfaz(idioma, "usuarios", "esc_usuario"),
            style={'width': '200px', 'marginRight': '10px'}
        ),
        dcc.Input(
            id='input-passwd',
            type='password',
            placeholder=bd.obtener_textos_interfaz(idioma, "usuarios", "esc_contrasena"),
            style={'width': '200px', 'marginRight': '10px'}
        ),
        dbc.Checkbox(
            id="check-admin",
            label="Admin",
            style={'marginRight': '15px', 'alignSelf': 'center'}
        ),
        html.Button(bd.obtener_textos_interfaz(idioma, "usuarios", "anadir"), id='add-usuario-button', n_clicks=0),
        dbc.Modal([
            dbc.ModalHeader(bd.obtener_textos_interfaz(idioma, "usuarios", "confirmacion")),
            dbc.ModalBody(bd.obtener_textos_interfaz(idioma, "usuarios", "msg_confirmacion_usu")),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="cancelar-anadir", className="ms-auto", n_clicks=0),
                dbc.Button("Añadir", id="confirmar-anadir", color="success", n_clicks=0),
            ]),
        ], id="modal-confirmacion-anadir", is_open=False),
        html.Div(id="mensaje-usuario", style={"marginTop": "10px"}),
    ], style={'display': 'flex', 'alignItems': 'center'}),
    html.Div(id="mensaje-anadir", style={"color": "red", "marginTop": "10px"}),
])
