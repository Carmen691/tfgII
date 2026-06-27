from dash import html, dcc
import dash_bootstrap_components as dbc

def layout_filtros():
    return dcc.Loading(
        id="loading-filtros",
        type="circle",
        children=html.Div([

            html.Div(id="filtros-container", children=[

                html.Div([
                    html.Label(id="tipo_entidad", className="filtros-label"),
                    dcc.Dropdown(
                        id="tipo-entidad-dropdown",
                        multi=False,
                        persistence=True,
                        persistence_type="session",
                        className="dropdown-pro"
                    )
                ], className="filtro-card"),

                html.Div([
                    html.Label(id="fecha_wcag", className="filtros-label"),
                    dcc.Dropdown(
                        id="version-auditoria-dropdown",
                        multi=False,
                        persistence=True,
                        persistence_type="session",
                        className="dropdown-pro"
                    )
                ], className="filtro-card"),

                html.Div([
                    html.Label(id="entidades", className="filtros-label"),
                    dcc.Dropdown(
                        id="entidad-dropdown",
                        multi=True,
                        searchable=True,
                        persistence=True,
                        persistence_type="session",
                        className="dropdown-pro"
                    )
                ], className="filtro-card"),

                html.Div([
                    html.Label(id="principios_wcag", className="filtros-label"),
                    dcc.Checklist(
                        id="principios-checklist",
                        className="checklist-pro"
                    )
                ], className="filtro-card"),

                html.Div([
                    html.Label(id="version_wcag", className="filtros-label"),
                    dcc.Checklist(
                        id="wcag-version-checklist",
                        className="checklist-pro"
                    )
                ], className="filtro-card"),

                html.Div([
                    html.Label(id="nivel", className="filtros-label"),
                    dcc.Checklist(
                        id="nivel-checklist",
                        className="checklist-pro"
                    )
                ], className="filtro-card"),


                html.Div([
                    html.Button(
                        id="boton-actualizar",
                        n_clicks=0,
                        className="btn-pro"
                    )
                ], className="filtros-actions")

            ]),

        ])
    )