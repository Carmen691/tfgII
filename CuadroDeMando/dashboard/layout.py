from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

external_stylesheets = [
    dbc.themes.BOOTSTRAP
]


def crear_layout():

    return html.Div(

        [

            dcc.Location(id="url", refresh=False),

            # =====================================================
            # STORES
            # =====================================================

            dcc.Store(id="menu-collapsed", data=False),

            dcc.Store(id="store-idioma", data="es"),

            dcc.Store(id="init-done", data=False),

            dcc.Store(id="app-initialized", data=False),

            dcc.Store(id="store-tipo-entidad", storage_type="session"),

            dcc.Store(id="store-principios", storage_type="session"),

            dcc.Store(id="store-versiones", storage_type="session"),

            dcc.Store(id="store-niveles", storage_type="session"),

            dcc.Store(id="store-entidad", storage_type="session"),

            dcc.Store(id="store-fecha", storage_type="session"),

            dcc.Store(id="tabla-actual-store", storage_type="session"),

            dcc.Store(id="auth-status", storage_type="session"),

            # =====================================================
            # INIT
            # =====================================================

            dcc.Interval(
                id="init-trigger",
                interval=1,
                n_intervals=0,
                max_intervals=1
            ),

            # =====================================================
            # TOP BAR
            # =====================================================

            html.Header(

            [

                html.Div(

                    [

                        html.Button(

                            DashIconify(
                                icon="tabler:menu-2",
                                width=22
                            ),

                            id="toggle-menu",

                            className="menu-toggle"

                        ),

                        html.Div(

                            [

                                DashIconify(
                                    icon="tabler:shield-check",
                                    width=32,
                                    color="#2563eb"
                                ),

                                html.Div(

                                    [

                                        html.Div(
                                            "Audit Dashboard",
                                            className="header-title"
                                        ),

                                        html.Div(
                                            "TFG",
                                            className="header-subtitle"
                                        )

                                    ],

                                    className="header-brand-text"

                                )

                            ],

                            className="header-brand"

                        ),

                    ],

                    className="header-left"

                ),

                    dmc.Select(

                        id="idioma-dropdown",

                        data=[
                            {
                                "label": "Español",
                                "value": "es"
                            },
                            {
                                "label": "English",
                                "value": "en"
                            },
                        ],

                        value="es",

                        clearable=False,

                        searchable=False,

                        radius="md",

                        size="sm",

                        w=150,

                    )

                ],

                className="topbar"

            ),

            # =====================================================
            # BODY
            # =====================================================

            html.Div(

                [

                    # =============================================
                    # SIDEBAR
                    # =============================================

                    html.Nav(

                        [

                            html.Div(

                                [

                                    dcc.Link(
                                        [],
                                        href="/dash/filtros",
                                        id="link-filtros",
                                        className="sidebar-link"
                                    ),

                                    dcc.Link(
                                        [],
                                        href="/dash/cuadroMando",
                                        id="link-cuadro",
                                        className="sidebar-link"
                                    ),

                                    dcc.Link(
                                        [],
                                        href="/dash/datos",
                                        id="link-datos",
                                        className="sidebar-link"
                                    ),

                                    dcc.Link(
                                        [],
                                        href="/dash/importar",
                                        id="link-importar",
                                        className="sidebar-link"
                                    ),

                                    html.Button(
                                        [],
                                        id="admin-toggle",
                                        className="sidebar-link sidebar-section",
                                        n_clicks=0,
                                    ),

                                    dbc.Collapse(

                                        [

                                            dcc.Link(
                                                [],
                                                href="/dash/administracion/usuarios",
                                                id="link-usuarios",
                                                className="sidebar-sublink"
                                            ),

                                            dcc.Link(
                                                [],
                                                href="/dash/administracion/auditorias",
                                                id="link-auditorias",
                                                className="sidebar-sublink"
                                            ),

                                        ],

                                        id="admin-collapse",

                                        is_open=False

                                    )

                                ],

                                className="menu-container"

                            ),

                            html.A(

                                [],

                                href="/logout",

                                id="logout-button",

                                className="sidebar-link logout"

                            )

                        ],

                        id="sidebar",

                        className="sidebar"

                    ),

                    # =============================================
                    # CONTENT
                    # =============================================

                    html.Main(

                        html.Div(

                            id="page-content",

                            className="page-content"

                        ),

                        id="main-content",

                        className="main"

                    )

                ],

                className="layout-body"

            )

        ]

    )