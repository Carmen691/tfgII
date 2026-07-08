from dash import html, dcc

def layout_gestion():
    return dcc.Loading(
        id="loading-gestion",
        type="circle",
        fullscreen=False,
        children=html.Div(
            className="gestion-container",
            children=[

                html.H2(
                    id="titulo-gestion",
                    className="gestion-titulo"
                ),

                html.Label(
                    id="label-auditorias",
                    className="gestion-label"
                ),

                dcc.Dropdown(
                    id="auditorias-dropdown",
                    className="gestion-dropdown"
                ),

                html.Label(
                    id="label-versiones",
                    className="gestion-label"
                ),

                dcc.Dropdown(
                    id="versiones-dropdown",
                    className="gestion-dropdown",
                    disabled=True
                ),

                html.Br(),

                html.Button(
                    id="borrar-auditoria-button",
                    n_clicks=0,
                    className="gestion-boton"
                ),

                html.Div(
                    id="mensaje-auditoria",
                    className="gestion-mensaje"
                ),
            ],
        ),
    )