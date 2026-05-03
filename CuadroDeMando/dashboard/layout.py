from dash import html, dcc
import dash_bootstrap_components as dbc

external_stylesheets = [
    dbc.themes.BOOTSTRAP
]


def crear_layout():
    return html.Div([

        dcc.Location(id='url', refresh=False),

        # =========================
        # STORES
        # =========================
        dcc.Store(id="menu-collapsed", data=False),
        dcc.Store(id='store-idioma', data='es'),
        dcc.Store(id='init-done', data=False),

        dcc.Store(id='store-data', storage_type='session'),
        dcc.Store(id='store-tipo-entidad', storage_type='session'),
        dcc.Store(id='store-principios', storage_type='session'),
        dcc.Store(id='store-versiones', storage_type='session'),
        dcc.Store(id='store-niveles', storage_type='session'),
        dcc.Store(id='store-entidad', storage_type='session'),
        dcc.Store(id="tabla-actual-store", storage_type='session'),

        # =========================
        # INIT
        # =========================
        dcc.Interval(
            id='init-trigger',
            interval=1,
            n_intervals=0,
            max_intervals=1
        ),

        # =========================
        # TOP BAR
        # =========================
        html.Div([

            html.Button(
                html.Span("▦", className="icon-panel"),
                id="toggle-menu",
                className="menu-toggle"
            ),

            html.Div(
                dcc.Dropdown(
                    id='idioma-dropdown',
                    options=[
                        {'label': 'Español', 'value': 'es'},
                        {'label': 'English', 'value': 'en'}
                    ],
                    value='es',
                    clearable=False,
                    className="lang-dropdown"
                ),
                className="topbar-right"
            )

        ], className="topbar"),

        # =========================
        # SIDEBAR
        # =========================
        html.Div([

            html.Div([

                dcc.Link([
                    html.Span("📊", className="icon"),
                    html.Span("Filtros", className="menu-text")
                ], href="/dash/filtros", className="sidebar-link", id="link-filtros"),

                dcc.Link([
                    html.Span("📈", className="icon"),
                    html.Span("Cuadro de mando", className="menu-text")
                ], href="/dash/cuadroMando", className="sidebar-link", id="link-cuadro"),

                dcc.Link([
                    html.Span("📋", className="icon"),
                    html.Span("Tabla de datos", className="menu-text")
                ], href="/dash/datos", className="sidebar-link", id="link-datos"),

                dcc.Link([
                    html.Span("📥", className="icon"),
                    html.Span("Importar", className="menu-text")
                ], href="/dash/importar", className="sidebar-link", id="link-importar"),

                html.Div([
                    html.Span("⚙️", className="icon"),
                    html.Span("Administración", className="menu-text")
                ],
                id="admin-toggle",
                className="sidebar-link sidebar-section"
                ),

                dbc.Collapse([

                    dcc.Link([
                        html.Span("👤", className="icon"),
                        html.Span("Usuarios", className="menu-text")
                    ], href="/dash/administracion/usuarios", className="sidebar-sublink", id="link-usuarios"),

                    dcc.Link([
                        html.Span("📑", className="icon"),
                        html.Span("Auditorías", className="menu-text")
                    ], href="/dash/administracion/auditorias", className="sidebar-sublink", id="link-auditorias"),

                ], id="admin-collapse", is_open=False),

            ], className="menu-container"),

            html.Button(
                [
                    html.Span("🚪", className="icon"),
                    html.Span("Cerrar sesión", className="menu-text")
                ],
                id="logout-button",
                className="sidebar-link logout",
                n_clicks=0
            )

        ],
        id="sidebar",
        className="sidebar"
        ),

        # =========================
        # MAIN CONTENT
        # =========================
        html.Div([

            dcc.Store(id="auth-status", storage_type="session"),

            html.Div(
                id='page-content',
                className="page-content"
            )

        ],
        id="main-content",
        className="main")

    ])