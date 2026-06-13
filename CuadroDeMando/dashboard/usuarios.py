from dash import html, dcc
import dash_bootstrap_components as dbc


def layout_usuarios():

    return dcc.Loading(
        id="loading-usuarios-page",
        type="circle",
        fullscreen=False,

        children=html.Div([

            # ---------------- ELIMINAR USUARIO ----------------

            html.Div([

                html.H2(
                    id="titulo-usuarios-eliminar"
                ),

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

                        dbc.ModalHeader(
                            id="modal-titulo-eliminar"
                        ),

                        dbc.ModalBody(
                            id="modal-texto-eliminar"
                        ),

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

                    ],
                        id="modal-confirmacion",
                        is_open=False
                    ),

                    html.Div(
                        id="mensaje-usuario-eliminar",
                        className="mensaje"
                    ),

                ],
                    className="fila-usuarios"
                ),

            ], id="admin-eliminar-wrapper"),


            # ---------------- AÑADIR USUARIO ----------------

            html.Div([

                html.H2(
                    id="titulo-usuarios-anadir"
                ),

                html.Div([

                    dcc.Input(
                        id='input-usuario',
                        type='text',
                        className="input-style"
                    ),

                    html.Div([
                        dcc.Input(
                            id='input-passwd',
                            type='password',
                            className="input-style"
                        ),
                        html.Button(
                            "👁",
                            id="ver-password-alta",
                            n_clicks=0,
                            className="ojo-password"
                        )
                    ], className="password-container"),

                    dbc.Checkbox(
                        id="check-admin",
                        label="Admin",
                        className="check-style"
                    ),

                    html.Button(
                        id='add-usuario-button',
                        n_clicks=0,
                        className="btn btn-success"
                    ),

                    dbc.Modal([

                        dbc.ModalHeader(
                            id="modal-titulo-anadir"
                        ),

                        dbc.ModalBody(
                            id="modal-texto-anadir"
                        ),

                        dbc.ModalFooter([

                            dbc.Button(
                                "Cancelar",
                                id="cancelar-anadir",
                                n_clicks=0
                            ),

                            dbc.Button(
                                "Añadir",
                                id="confirmar-anadir",
                                color="success",
                                n_clicks=0
                            ),

                        ]),

                    ],
                        id="modal-confirmacion-anadir",
                        is_open=False
                    ),

                    html.Div(
                        id="mensaje-usuario-anadir",
                        className="mensaje"
                    ),

                ],
                    className="fila-usuarios"
                ),

            ], id="admin-anadir-wrapper"),


            # ---------------- CAMBIAR PASSWORD ----------------

            html.Div([

                html.H2(
                    id="titulo-cambiar-password"
                ),

                html.Div([
                    html.Div([
                        dcc.Input(
                        id='input-password-actual',
                        type='password',
                        className="input-style"
                        ),

                        html.Button(
                            "👁",
                            id="ver-password-actual",
                            n_clicks=0,
                            className="ojo-password"
                        )
                    ],
                    className="password-container"),

                    html.Div([
                        dcc.Input(
                            id='input-password-nueva',
                            type='password',
                            className="input-style"
                        ),

                        html.Button(
                            "👁",
                            id="ver-password-nueva",
                            n_clicks=0,
                            className="ojo-password"
                        )
                    ],
                    className="password-container"),

                    html.Div([
                        dcc.Input(
                        id='input-password-confirmar',
                        type='password',
                        className="input-style"
                        ),

                        html.Button(
                            "👁",
                            id="ver-password-confirmar",
                            n_clicks=0,
                            className="ojo-password"
                        )
                    ],
                    className="password-container"),

                    html.Button(
                        id='cambiar-password-button',
                        n_clicks=0,
                        className="btn btn-success"
                    ),

                    dbc.Modal([

                        dbc.ModalHeader(
                            id="btn-confirmar-cambio"
                        ),

                        dbc.ModalBody(
                            id="body-confirmar-cambio"
                        ),

                        dbc.ModalFooter([

                            dbc.Button(
                                id="cancelar-password",
                                n_clicks=0
                            ),

                            dbc.Button(
                                id="confirmar-password",
                                color="success",
                                n_clicks=0
                            ),

                        ])

                    ],
                        id="modal-confirmacion-password",
                        is_open=False
                    ),

                    html.Div(
                        id="mensaje-password",
                        className="mensaje"
                    ),

                ],
                    className="fila-usuarios"
                ),

            ], id="password-wrapper"),

        ],
            className="main-card"
        )
    )