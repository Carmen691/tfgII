from dash import html, dcc
import dash_bootstrap_components as dbc

def layout_usuarios():
    return dcc.Loading(
        id="loading-usuarios-page",
        type="circle",
        fullscreen=False,
        children=html.Div([

            html.H2(id="titulo-usuarios-eliminar"),

            html.Div([

                html.Label(
                    id="label-usuarios",
                    className="label-filtro"
                ),

                dcc.Dropdown(
                    id='usuarios-dropdown',
                    style={"width": "300px"}
                ),

                html.Button(
                    id='borrar-usuario-button',
                    n_clicks=0,
                ),

                dbc.Modal([
                    dbc.ModalHeader(id="modal-titulo-eliminar"),
                    dbc.ModalBody(id="modal-texto-eliminar"),
                    dbc.ModalFooter([
                        dbc.Button(
                            id="cancelar-eliminar",
                            className="boton-azul",
                            n_clicks=0
                        ),
                        dbc.Button(
                            id="confirmar-eliminar",
                            color="danger",
                            n_clicks=0
                        ),
                    ])
                ], id="modal-confirmacion", is_open=False),

                html.Div(id="mensaje-usuario-eliminar", className="mensaje"),

            ], className="fila-usuarios"),

            html.H2(id="titulo-usuarios-anadir"),

            html.Div([

                dcc.Input(
                    id='input-usuario',
                    type='text',
                    className="input-style"
                ),

                dcc.Input(
                    id='input-passwd',
                    type='password',
                    className="input-style"
                ),

                dbc.Checkbox(
                    id="check-admin",
                    label="Admin",
                    className="check-style"
                ),

                html.Button(
                    id='add-usuario-button',
                    n_clicks=0,
                    className="btn-success"
                ),

                dbc.Modal([
                    dbc.ModalHeader(id="modal-titulo-anadir"),
                    dbc.ModalBody(id="modal-texto-anadir"),
                    dbc.ModalFooter([
                        dbc.Button("Cancelar", id="cancelar-anadir", n_clicks=0),
                        dbc.Button("Añadir", id="confirmar-anadir", color="success", n_clicks=0),
                    ]),
                ], id="modal-confirmacion-anadir", is_open=False),

                html.Div(id="mensaje-usuario-anadir", className="mensaje"),

            ], className="fila-usuarios"),

        ], className="main-card"))