# dashboard/layout.py
from dash import html, dcc, dash_table


def crear_layout(df, idioma, entidades, fig):
    return html.Div([
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
                dcc.Link("Dashboard", href="/dash/", style={"display": "block", "padding": "10px", "color": "white"}),
                dcc.Link("Tabla de datos", href="/dash/datos", style={"display": "block", "padding": "10px", "color": "white"}),
                html.A("Cerrar sesión", href="/logout", target="_self", className="nav-link")
            ], id="menu-content")
        ], id="sidebar", style={
            "position": "fixed", "top": "0", "left": "0",
            "width": "250px", "height": "100%",
            "backgroundColor": "#2c3e50", "paddingTop": "20px",
            "zIndex": "1000", "overflow": "hidden"
        }),

        # Contenido principal
        html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content', style={'width': '80%', 'padding': '20px'})
        ], id="main-content", style={"marginLeft": "260px", "padding": "20px"})
    ])

