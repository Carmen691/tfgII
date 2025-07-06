from dash import html, dcc

def layout_graficos(fig, figPorcentaje, figMapaCalor):
    return html.Div([
        html.H2("Bienvenido al Dashboard"),
        dcc.Graph(id='grafico-general', figure=fig),
        dcc.Graph(id='grafico-porcentaje', figure=figPorcentaje),
        dcc.Graph(id='grafico-mapa-calor', figure=figMapaCalor)
    ])
