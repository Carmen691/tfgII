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
        dcc.Store(id="app-initialized", data=False),
        dcc.Store(id='store-data', storage_type='session'),
        dcc.Store(id='store-filtros-posibles', storage_type='session'),
        dcc.Store(id='store-tipo-entidad', storage_type='session'),
        dcc.Store(id='store-principios', storage_type='session'),
        dcc.Store(id='store-versiones', storage_type='session'),
        dcc.Store(id='store-niveles', storage_type='session'),
        dcc.Store(id='store-entidad', storage_type='session'),
        dcc.Store(id="store-fecha", storage_type='session'),
        dcc.Store(id="tabla-actual-store", storage_type='session'),
        #dcc.Interval(id='session-check', interval=60*1000, n_intervals=0),

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
                ], href="/dash/filtros", className="sidebar-link", id="link-filtros"),

                dcc.Link([
                    html.Span("📈", className="icon"),
                ], href="/dash/cuadroMando", className="sidebar-link", id="link-cuadro"),

                dcc.Link([
                    html.Span("📋", className="icon"),
                ], href="/dash/datos", className="sidebar-link", id="link-datos"),

                dcc.Link([
                    html.Span("📥", className="icon"),
                ], href="/dash/importar", className="sidebar-link", id="link-importar"),

                html.Div([
                    html.Span("⚙️", className="icon"),
                ],
                id="admin-toggle",
                className="sidebar-link sidebar-section"
                ),

                dbc.Collapse([

                    dcc.Link([
                        html.Span("👤", className="icon"),
                    ], href="/dash/administracion/usuarios", className="sidebar-sublink", id="link-usuarios"),

                    dcc.Link([
                        html.Span("📑", className="icon"),
                    ], href="/dash/administracion/auditorias", className="sidebar-sublink", id="link-auditorias"),

                ], id="admin-collapse", is_open=False),

            ], className="menu-container"),

            html.A(
                [
                    html.Span("🚪", className="icon"),
                ],
                href="/logout",
                id="logout-button",
                className="sidebar-link logout"
            ),

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