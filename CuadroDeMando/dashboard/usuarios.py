from dash import html, dcc
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
                                            disabled=True,
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

                                dmc.Modal(

                                    id="modal-confirmacion",

                                    opened=False,

                                    centered=True,

                                    withCloseButton=False,

                                    closeOnClickOutside=False,

                                    closeOnEscape=False,

                                    radius="lg",

                                    size="md",

                                    title=dmc.Group(

                                        [

                                            DashIconify(
                                                icon="tabler:alert-triangle",
                                                width=22,
                                                color="#dc2626"
                                            ),

                                            html.Span(
                                                id="modal-titulo-eliminar"
                                            ),

                                        ],

                                        gap="sm",

                                    ),

                                    children=[

                                        html.Div(
                                            id="modal-texto-eliminar",
                                            style={
                                                "paddingBottom": "20px"
                                            }
                                        ),

                                        dmc.Group(

                                            [

                                                dmc.Button(
                                                    id="cancelar-eliminar",
                                                    variant="default",
                                                    radius="md",
                                                ),

                                                dmc.Button(
                                                    id="confirmar-eliminar",
                                                    color="red",
                                                    radius="md",
                                                ),

                                            ],

                                            justify="flex-end",

                                        ),

                                    ],

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
                                            disabled=True,
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

                                dmc.Modal(

                                    id="modal-confirmacion-anadir",

                                    opened=False,

                                    centered=True,

                                    withCloseButton=False,

                                    closeOnClickOutside=False,

                                    closeOnEscape=False,

                                    radius="lg",

                                    size="md",

                                    title=dmc.Group(

                                        [

                                            DashIconify(
                                                icon="tabler:user-plus",
                                                width=22,
                                                color="#2563eb"
                                            ),

                                            html.Span(
                                                id="modal-titulo-anadir"
                                            ),

                                        ],

                                        gap="sm",

                                    ),

                                    children=[

                                        html.Div(
                                            id="modal-texto-anadir",
                                            style={
                                                "paddingBottom": "20px"
                                            }
                                        ),

                                        dmc.Group(

                                            [

                                                dmc.Button(
                                                    id="cancelar-anadir",
                                                    variant="default",
                                                    radius="md",
                                                ),

                                                dmc.Button(
                                                    id="confirmar-anadir",
                                                    color="blue",
                                                    radius="md",
                                                ),

                                            ],

                                            justify="flex-end",

                                        ),

                                    ],

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
                                            disabled=True,
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

                                dmc.Modal(

                                    id="modal-confirmacion-password",

                                    opened=False,

                                    centered=True,

                                    withCloseButton=False,

                                    closeOnClickOutside=False,

                                    closeOnEscape=False,

                                    radius="lg",

                                    size="md",

                                    title=dmc.Group(

                                        [

                                            DashIconify(
                                                icon="tabler:key",
                                                width=22,
                                                color="#16a34a"
                                            ),

                                            html.Span(
                                                id="btn-confirmar-cambio"
                                            ),

                                        ],

                                        gap="sm",

                                    ),

                                    children=[

                                        html.Div(
                                            id="body-confirmar-cambio",
                                            style={
                                                "paddingBottom": "20px"
                                            }
                                        ),

                                        dmc.Group(

                                            [

                                                dmc.Button(
                                                    id="cancelar-password",
                                                    variant="default",
                                                    radius="md",
                                                ),

                                                dmc.Button(
                                                    id="confirmar-password",
                                                    color="green",
                                                    radius="md",
                                                ),

                                            ],

                                            justify="flex-end",

                                        ),

                                    ],

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