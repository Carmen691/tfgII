from dash import html, dcc
import data.querys as dq

def layout_graficos(idioma_sel, figPrincipios, figPorcentaje, figNiveles, tipoEntidad):
    return html.Div([

        html.Div(
            children=[
                html.Div("Medición: Ayuntamientos", style={
                    "background": "#eef2ff",
                    "padding": "6px 14px",
                    "border-radius": "10px",
                    "font-size": "14px"
                }),
                html.Div("Versión WCAG: 2.0", style={
                    "background": "#ecfeff",
                    "padding": "6px 14px",
                    "border-radius": "10px",
                    "font-size": "14px"
                }),
            ],
            style={
                "display": "flex",
                "justify-content": "center",   # 🔥 cambio importante
                "gap": "15px",                 # separación bonita
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
                children=[
                    html.H4("DATOS WCAG"),
                    html.P("Total Entidades: " + str(dq.obtener_numero_entidades(tipoEntidad))),
                    html.P("Total Mediciones: " + str(dq.obtener_numero_mediciones(tipoEntidad))),
                    html.P("Cumplimientos: " + str(dq.obtener_numero_cumplimientos(tipoEntidad))),
                    html.P("Porcentaje Cumplimiento: " + str(dq.obtener_porcentaje_cumplimiento(tipoEntidad)))
                ],
                style=card_style
            ),

            html.Div(id="cumplimiento-div",
                style=card_style
            ),

            html.Div(
                children=[
                    html.H4("% Por niveles"),
                    html.P("A: %"),
                    html.P("AA: %"),
                    html.P("AAA: %"),
                ],
                style=card_style
            )

        ], style={
            "display": "flex",
            "gap": "15px",
            "flex-wrap": "wrap"  
        }),

        dcc.Graph(id='grafico-porcentaje', figure=figPorcentaje),
        dcc.Graph(id='grafico-principios', figure=figPrincipios),
        dcc.Graph(id='grafico-niveles', figure=figNiveles),
    ])


card_style = {
    "border": "1px solid #ccc",
    "border-radius": "10px",
    "padding": "15px",
    "width": "250px",
    "text-align": "center",
    "box-shadow": "2px 2px 10px rgba(0,0,0,0.1)"
}