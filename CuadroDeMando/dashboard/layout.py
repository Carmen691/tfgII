# dashboard/layout.py
from dash import html, dcc
import dash_bootstrap_components as dbc

external_stylesheets = [
    dbc.themes.BOOTSTRAP
]


def crear_layout():
    return html.Div([

        dcc.Location(id='url', refresh=False),

        # =========================
        # 🔵 STORES DE ESTADO
        # =========================
        dcc.Store(id="menu-collapsed", data=False),
        dcc.Store(id='store-idioma', data='es'),
        dcc.Store(id='init-done', data=False),  # 👈 IMPORTANTE

        dcc.Store(id='store-data', storage_type='session'),
        dcc.Store(id='store-tipo-entidad', storage_type='session'),
        dcc.Store(id='store-principios', storage_type='session'),
        dcc.Store(id='store-versiones', storage_type='session'),
        dcc.Store(id='store-niveles', storage_type='session'),
        dcc.Store(id='store-entidad', storage_type='session'),
        dcc.Store(id="tabla-actual-store", storage_type='session'),

        # =========================
        # INIT TRIGGER
        # =========================
        dcc.Interval(
            id='init-trigger',
            interval=1,
            n_intervals=0,
            max_intervals=1
        ),

        # =========================
        # BAR TOP
        # =========================
        html.Div([

            html.Button(
                "⮜",
                id="toggle-menu",
                style={
                    "position": "absolute",
                    "top": "10px",
                    "left": "10px",
                    "zIndex": "1100",
                    "backgroundColor": "#ffffff",
                    "color": "#2c3e50",
                    "border": "none",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 6px rgba(0, 0, 0, 0.3)",
                    "padding": "10px 14px",
                    "cursor": "pointer",
                    "fontSize": "20px"
                }
            ),

            dcc.Dropdown(
                id='idioma-dropdown',
                options=[
                    {'label': 'Español', 'value': 'es'},
                    {'label': 'English', 'value': 'en'}
                ],
                value='es',
                clearable=False,
                style={
                    "width": "100px",
                    "marginLeft": "auto",
                    "marginRight": "10px"
                }
            )

        ], style={
            "position": "relative",
            "height": "50px",
            "marginBottom": "10px"
        }),

        # =========================
        # SIDEBAR (CONTROLADO)
        # =========================
        html.Div([

            html.H2("Menú", className="sidebar-title", id="titulo-menu"),

            dcc.Link("Filtros", id="link-filtros", href="/dash/filtros", className="sidebar-link"),
            dcc.Link("Cuadro", id="link-cuadro", href="/dash/cuadroMando", className="sidebar-link"),
            dcc.Link("Datos", id="link-datos", href="/dash/datos", className="sidebar-link"),
            dcc.Link("Importar", id="link-importar", href="/dash/importar", className="sidebar-link"),

            html.Div(
                id="admin-toggle",
                className="sidebar-link",
                n_clicks=0,
                style={"cursor": "pointer"}
            ),

            dbc.Collapse([
                dcc.Link(
                    "Usuarios",
                    id="link-usuarios",
                    href="/dash/administracion/usuarios",
                    className="sidebar-sublink"
                ),

                dcc.Link(
                    "Auditorías",
                    id="link-auditorias",
                    href="/dash/administracion/auditorias",
                    className="sidebar-sublink"
                ),
            ],
            id="admin-collapse",
            is_open=False),

            html.Button(
                id="logout-button",
                className="nav-link",
                n_clicks=0
            )

        ],
        id="sidebar",
        style={"display": "none"}  # 👈 OCULTO AL INICIO
        ),

        # =========================
        # CONTENIDO PRINCIPAL
        # =========================
        html.Div([

            dcc.Store(
                id="auth-status",
                storage_type="session"
            ),

            html.Div(
                id='page-content',
                style={
                    'width': '100%',
                    'padding': '20px'
                }
            )

        ],
        id="main-content",
        style={
            "marginLeft": "260px",
            "padding": "20px"
        })

    ])