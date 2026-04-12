# dashboard/layout.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

from start.callbacks.services.data_services import cargar_datos

# external_stylesheets = [
#     "https://codepen.io/chriddyp/pen/bWLwgP.css"
# ]
external_stylesheets = [
    dbc.themes.BOOTSTRAP
]

def crear_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        # Estado del menú (colapsado o no)
        dcc.Store(id="menu-collapsed", data=False),
        dcc.Store(id='store-idioma', data='es'),  # Store global para idioma
        dcc.Store(id='store-data', storage_type='session'),
        dcc.Store(id='store-tipo-entidad', storage_type='session'),
        dcc.Store(id='store-principios', storage_type='session'),
        dcc.Store(id='store-versiones', storage_type='session'),
        dcc.Store(id='store-niveles', storage_type='session'),
        dcc.Store(id='init-done', storage_type='session'),
        dcc.Store(id='entidad-store', storage_type='session'),
        dcc.Interval(id='init-trigger', interval=1, n_intervals=0, max_intervals=1),

        # Barra superior (header)
        html.Div([
            # Botón de menú colapsable (izquierda)
            html.Button("⮜", id="toggle-menu", style={
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
            }),

            # Selector de idioma (derecha)
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
        ], style={"position": "relative", "height": "50px", "marginBottom": "10px"}),

        # Menú lateral con botón
        html.Div([
            html.H2("Menú", className="sidebar-title"),
            dcc.Link("Filtros", href="/dash/filtros", className="sidebar-link", id="link-filtros"),
            dcc.Link("Cuadro de mando", href="/dash/cuadroMando", className="sidebar-link", id="link-cuadro"),
            dcc.Link("Tabla de datos", href="/dash/datos", className="sidebar-link", id="link-datos"),
            dcc.Link("Importar datos", href="/dash/importar", className="sidebar-link", id="link-importar"),

            html.Div([
                html.Span("Panel de administración", className="sidebar-admin-text"),
                html.I(className="bi bi-chevron-down sidebar-admin-icon", style={"float": "right"})
            ], 
            id="admin-toggle",
            className="sidebar-link", 
            n_clicks=0,
            style={"cursor": "pointer"}),
            dbc.Collapse([
                dcc.Link("Usuarios", href="/dash/administracion/usuarios", className="sidebar-sublink", id="link-usuarios"),
                dcc.Link("Gestión de auditorías", href="/dash/administracion/auditorias", className="sidebar-sublink", id="link-auditorias"),
            ], id="admin-collapse", is_open=False),
            html.A("Cerrar sesión", href="/logout", target="_self", className="nav-link")
        ], id="sidebar"),

        # Contenido principal
        html.Div([
            dcc.Store(id="auth-status", storage_type="session"),
            html.Div(id='page-content', style={'width': '100%', 'padding': '20px'})
        ], id="main-content", style={"marginLeft": "260px", "padding": "20px"})
    ])
