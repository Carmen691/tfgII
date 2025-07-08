from dash import html, dcc
import dash_bootstrap_components as dbc

def layout_usuarios(idioma, usuarios):
    return html.Div([
        html.H2("Eliminar usuarios"),

        html.Div([
            html.Label("Usuarios:", style={'marginRight': '10px', 'alignSelf': 'center'}),
            dcc.Dropdown(
                id='usuarios-dropdown',
                placeholder="Selecciona...",
                options=[{'label': usu, 'value': usu} for usu in usuarios["usuario"].unique()],
                style={'width': '300px', 'marginRight': '10px'}
            ),
            html.Button('Eliminar', id='borrar-usuario-button', n_clicks=0),
            dbc.Modal([
                dbc.ModalHeader("Confirmación"),
                dbc.ModalBody("¿Estás seguro de que deseas eliminar este usuario?"),
                dbc.ModalFooter([
                    dbc.Button("Cancelar", id="cancelar-eliminar", className="ms-auto", n_clicks=0),
                    dbc.Button("Eliminar", id="confirmar-eliminar", color="danger", n_clicks=0),
                ])
            ], id="modal-confirmacion", is_open=False),
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '15px'}),

        html.H2("Añadir usuarios"),
        html.Div([
        dcc.Input(
            id='input-usuario',
            type='text',
            placeholder='Escribe el usuario...',
            style={'width': '200px', 'marginRight': '10px'}
        ),
        dcc.Input(
            id='input-passwd',
            type='password',
            placeholder='Escribe la contraseña...',
            style={'width': '200px', 'marginRight': '10px'}
        ),
        dbc.Checkbox(
            id="check-admin",
            label="Administrador",
            style={'marginRight': '15px', 'alignSelf': 'center'}
        ),
        html.Button('Añadir', id='add-usuario-button', n_clicks=0),
        dbc.Modal([
            dbc.ModalHeader("Confirmación"),
            dbc.ModalBody("¿Estás seguro de que deseas añadir este usuario?"),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="cancelar-anadir", className="ms-auto", n_clicks=0),
                dbc.Button("Añadir", id="confirmar-anadir", color="success", n_clicks=0),
            ]),
        ], id="modal-confirmacion-anadir", is_open=False),
        html.Div(id="mensaje-usuario", style={"marginTop": "10px"}),
    ], style={'display': 'flex', 'alignItems': 'center'}),
    html.Div(id="mensaje-anadir", style={"color": "red", "marginTop": "10px"}),


])
