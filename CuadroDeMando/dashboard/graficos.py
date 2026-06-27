from dash import html, dcc
import data.querys as qr

def layout_graficos():
    return dcc.Loading(
        id="loading-graficos",
        type="circle",
        fullscreen=False,
        children=html.Div([

            html.Div(
                children=[
                    html.Div(id="nombre_medicion", style={
                        "background": "#eef2ff",
                        "padding": "6px 14px",
                        "border-radius": "10px",
                        "font-size": "14px"
                    }),
                    html.Div(id="version_medicion", style={
                        "background": "#ecfeff",
                        "padding": "6px 14px",
                        "border-radius": "10px",
                        "font-size": "14px"
                    }),
                ],
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "gap": "15px",
                    "align-items": "center",
                    "border": "1px solid #e5e7eb",
                    "border-radius": "12px",
                    "padding": "12px",
                    "background": "white",
                    "box-shadow": "0 4px 12px rgba(0,0,0,0.06)",
                    "margin-bottom": "20px"
                }
            ),

            html.Div([
                html.Div(
                    id="datos-wcag-div",
                    style=card_style
                ),

                html.Div(
                    id="cumplimiento-div",
                    style=card_style
                ),

                html.Div(
                    id="niveles-div",
                    style=card_style
                )

            ], style={
                "display": "flex",
                "gap": "15px",
                "flex-wrap": "wrap"
            }),

            dcc.Graph(id='grafico-porcentaje'),
            dcc.Graph(id='grafico-principios'),
            dcc.Graph(id='grafico-niveles'),

        ])
    )


card_style = {
    "border": "1px solid #ccc",
    "border-radius": "10px",
    "padding": "15px",
    "width": "250px",
    "text-align": "center",
    "box-shadow": "2px 2px 10px rgba(0,0,0,0.1)"
}