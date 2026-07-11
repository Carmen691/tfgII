from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc


def layout_usuarios():

    return dcc.Loading(
        id="loading-usuarios-page",
        type="circle",
        fullscreen=False,

        children=html.Div(

            [

                html.H2(
                    id="titulo-usuarios",
                    className="usuarios-titulo"
                ),

                # =====================================================
                # ELIMINAR USUARIO
                # =====================================================

                html.Div(

                    [

                        html.H3(
                            id="titulo-usuarios-eliminar",
                            className="usuarios-subtitulo"
                        ),

                        html.Div(

                            [

                                # ---------------- CAMPOS ----------------

                                html.Div(

                                    [

                                        dmc.Select(
                                            id="usuarios-dropdown",
                                            data=[],
                                            searchable=True,
                                            clearable=True,
                                            radius="md",
                                            size="md",
                                            w=300,
                                        ),

                                    ],

                                    className="fila-usuarios"

                                ),

                                # ---------------- BOTÓN ----------------

                                html.Div(

                                    [

                                        dmc.Button(
                                            id="borrar-usuario-button",
                                            n_clicks=0,
                                            variant="outline",
                                            color="red",
                                            radius="md",
                                            size="md",
                                            w=250,
                                            leftSection=DashIconify(
                                                icon="tabler:trash",
                                                width=18
                                            ),
                                        ),

                                        html.Div(
                                            id="mensaje-usuario-eliminar",
                                            className="mensaje"
                                        ),

                                    ],

                                    className="boton-con-mensaje"

                                ),

                                dbc.Modal(

                                    [

                                        dbc.ModalHeader(
                                            id="modal-titulo-eliminar"
                                        ),

                                        dbc.ModalBody(
                                            id="modal-texto-eliminar"
                                        ),

                                        dbc.ModalFooter(

                                            [

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

                                            ]

                                        ),

                                    ],

                                    id="modal-confirmacion",
                                    is_open=False,

                                ),

                            ],

                            className="usuarios-bloque",

                        ),

                    ],

                    id="admin-eliminar-wrapper",

                ),

                # =====================================================
                # AÑADIR USUARIO
                # =====================================================

                html.Div(

                    [

                        html.H3(
                            id="titulo-usuarios-anadir",
                            className="usuarios-subtitulo"
                        ),

                        html.Div(

                            [

                                html.Div(

                                    [

                                        dmc.TextInput(
                                            id="input-usuario",
                                            radius="md",
                                            size="md",
                                            w=300,
                                        ),

                                        dmc.PasswordInput(
                                            id="input-passwd",
                                            radius="md",
                                            size="md",
                                            w=300,
                                        ),

                                        html.Div(

                                            dmc.Checkbox(
                                                id="check-admin",
                                                label="Administrador",
                                                size="md",
                                                color="blue",
                                            ),

                                            className="checkbox-admin"

                                        ),

                                    ],

                                    className="fila-usuarios"

                                ),

                                html.Div(

                                    [

                                        dmc.Button(
                                            id="add-usuario-button",
                                            n_clicks=0,
                                            variant="outline",
                                            color="blue",
                                            radius="md",
                                            size="md",
                                            w=250,
                                            leftSection=DashIconify(
                                                icon="tabler:user-plus",
                                                width=18
                                            ),
                                        ),

                                        html.Div(
                                            id="mensaje-usuario-anadir",
                                            className="mensaje"
                                        ),

                                    ],

                                    className="boton-con-mensaje"

                                ),

                                dbc.Modal(

                                    [

                                        dbc.ModalHeader(
                                            id="modal-titulo-anadir"
                                        ),

                                        dbc.ModalBody(
                                            id="modal-texto-anadir"
                                        ),

                                        dbc.ModalFooter(

                                            [

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

                                            ]

                                        ),

                                    ],

                                    id="modal-confirmacion-anadir",
                                    is_open=False,

                                ),

                            ],

                            className="usuarios-bloque",

                        ),

                    ],

                    id="admin-anadir-wrapper",

                ),

                # =====================================================
                # CAMBIAR PASSWORD
                # =====================================================

                html.Div(

                    [

                        html.H3(
                            id="titulo-cambiar-password",
                            className="usuarios-subtitulo"
                        ),

                        html.Div(

                            [

                                html.Div(

                                    [

                                        dmc.PasswordInput(
                                            id="input-password-actual",
                                            radius="md",
                                            size="md",
                                            w=300,
                                        ),

                                        dmc.PasswordInput(
                                            id="input-password-nueva",
                                            radius="md",
                                            size="md",
                                            w=300,
                                        ),

                                        dmc.PasswordInput(
                                            id="input-password-confirmar",
                                            radius="md",
                                            size="md",
                                            w=300,
                                        ),

                                    ],

                                    className="fila-usuarios"

                                ),

                                html.Div(

                                    [

                                        dmc.Button(
                                            id="cambiar-password-button",
                                            n_clicks=0,
                                            variant="outline",
                                            color="green",
                                            radius="md",
                                            size="md",
                                            w=250,
                                            leftSection=DashIconify(
                                                icon="tabler:key",
                                                width=18
                                            ),
                                        ),

                                        html.Div(
                                            id="mensaje-password",
                                            className="mensaje"
                                        ),

                                    ],

                                    className="boton-con-mensaje"

                                ),

                                dbc.Modal(

                                    [

                                        dbc.ModalHeader(
                                            id="btn-confirmar-cambio"
                                        ),

                                        dbc.ModalBody(
                                            id="body-confirmar-cambio"
                                        ),

                                        dbc.ModalFooter(

                                            [

                                                dbc.Button(
                                                    id="cancelar-password",
                                                    n_clicks=0
                                                ),

                                                dbc.Button(
                                                    id="confirmar-password",
                                                    color="success",
                                                    n_clicks=0
                                                ),

                                            ]

                                        ),

                                    ],

                                    id="modal-confirmacion-password",
                                    is_open=False,

                                ),

                            ],

                            className="usuarios-bloque",

                        ),

                    ],

                    id="password-wrapper",

                ),

            ],

            className="usuarios-container",

        ),

    )