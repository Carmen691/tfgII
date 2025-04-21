from dash import html, dcc

def layout_graficos(fig):
    return html.Div([
        html.H2("Bienvenido al Dashboard"),
        dcc.Graph(figure=fig)
    ])
