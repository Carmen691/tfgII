# dashboard/layout.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.10.5/font/bootstrap-icons.min.css"
]

def crear_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        # Estado del menú (colapsado o no)
        dcc.Store(id="menu-collapsed", data=False),

        # Menú lateral con botón
        html.Div([
            # Botón de colapso (siempre visible)
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


            # Contenido del menú
            html.Div([
                html.H2("", style={"color": "white", "padding": "20px"}),
                dcc.Link("Filtros", href="/dash/filtros", style={"display": "block", "padding": "10px", "color": "white"}),
                dcc.Link("Cuadro de mando", href="/dash/cuadroMando", style={"display": "block", "padding": "10px", "color": "white"}),
                dcc.Link("Tabla de datos", href="/dash/datos", style={"display": "block", "padding": "10px", "color": "white"}),
                dcc.Link("Importar datos", href="/dash/importar", style={"display": "block", "padding": "10px", "color": "white"}),
                html.Div([
                    html.Span("Panel de administración", style={"marginRight": "10px", "color": "white"}),
                    html.I(className="bi bi-chevron-down", style={"color": "white"})
                ],
                id="admin-toggle",  
                n_clicks=0,                
                style={
                    "width": "100%",
                    "padding": "10px",
                    "cursor": "pointer",
                    "backgroundColor": "#444",
                    "color": "white",
                    "marginTop": "10px"
                }),

                # Collapse con submenú
                dbc.Collapse([
                    dcc.Link("Usuarios", href="/dash/administracion/usuarios", style={"display": "block", "padding": "10px 10px 10px 30px", "color": "white"}),
                    dcc.Link("Gestión de auditorías", href="/dash/administracion/auditorias", style={"display": "block", "padding": "10px 10px 10px 30px", "color": "white"}),
                ], id="admin-collapse", is_open=False),
            html.A("Cerrar sesión", href="/logout", target="_self", className="nav-link", style={"display": "block", "padding": "10px", "color": "white"})
            ], id="menu-content")
        ], id="sidebar", style={
            "position": "fixed", "top": "0", "left": "0",
            "width": "250px", "height": "100%",
            "backgroundColor": "#2c3e50", "paddingTop": "20px",
            "zIndex": "1000", "overflow": "hidden"
        }),

        # Contenido principal
        html.Div([
            dcc.Store(id="auth-status", storage_type="session"),
            html.Div(id='page-content', style={'width': '80%', 'padding': '20px'})
        ], id="main-content", style={"marginLeft": "260px", "padding": "20px"})
    ])

