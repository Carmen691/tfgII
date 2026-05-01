from dash import html, dcc

def layout_datos():
    return dcc.Loading(
        id="loading-datos",
        type="circle",
        fullscreen=False,
        children=html.Div([

            html.Div(id="tabla-datos-container"),

            html.Button(
                id="btn-guardar-tabla",
                n_clicks=0
            ),

            html.Div(
                id="mensaje-guardar",
                style={"marginTop": "10px"}
            )
        ])
    )