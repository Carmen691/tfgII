from dash import html, dcc
import data.querys as dq

def layout_graficos(figPrincipios, figPorcentaje, figNiveles, tipoEntidad):
    return html.Div([
        html.Div([
            html.Div(
                children=[
                    html.H4("DATOS WCAG", style={"margin-bottom": "10px"}),
                    html.P("Total Entidades: " + str(dq.obtener_numero_entidades(tipoEntidad))),
                    html.P("Total Mediciones: 120"),
                    html.P("Cumplimientos: 85"),
                    html.P("Porcentaje Cumplimiento: 70.8%"),
                ],
                style={
                    "border": "1px solid #ccc",
                    "border-radius": "10px",
                    "padding": "15px",
                    "width": "250px",
                    "text-align": "center",
                    "box-shadow": "2px 2px 10px rgba(0,0,0,0.1)"
                }
            ),
            html.Div(
                children=[
                    html.H4("Resumen", style={"margin-bottom": "10px"}),
                    html.P("Medición: Ayuntamientos"),
                    html.P("Versión WCAG: 2.0"),
                ],
                style={
                    "border": "1px solid #ccc",
                    "border-radius": "10px",
                    "padding": "15px",
                    "width": "250px",
                    "text-align": "center",
                    "box-shadow": "2px 2px 10px rgba(0,0,0,0.1)"
                }
            ),
                                html.Div(
                children=[
                    html.H4("% Cumplimiento", style={"margin-bottom": "10px"}),
                    html.P("Operable: %"),
                    html.P("Comprensible: %"),
                    html.P("Robusto: %"),
                    html.P("Perceptible: %"),
                ],
                style={
                    "border": "1px solid #ccc",
                    "border-radius": "10px",
                    "padding": "15px",
                    "width": "250px",
                    "text-align": "center",
                    "box-shadow": "2px 2px 10px rgba(0,0,0,0.1)"
                }
            ),
                                html.Div(
                children=[
                    html.H4("% Por niveles", style={"margin-bottom": "10px"}),
                    html.P("A: %"),
                    html.P("AA: %"),
                    html.P("AAA: %"),
                ],
                style={
                    "border": "1px solid #ccc",
                    "border-radius": "10px",
                    "padding": "15px",
                    "width": "250px",
                    "text-align": "center",
                    "box-shadow": "2px 2px 10px rgba(0,0,0,0.1)"
                }
            )
            ], style={
            "display": "flex",
            "gap": "15px",              # espacio entre tarjetas
        }),
        #dcc.Graph(id='grafico-general', figure=fig),
        dcc.Graph(id='grafico-porcentaje', figure=figPorcentaje),
        dcc.Graph(id='grafico-principios', figure=figPrincipios),
        dcc.Graph(id='grafico-niveles', figure=figNiveles),
        #dcc.Graph(id='grafico-mapa-calor', figure=figMapaCalor),
        # html.H4("Estadísticas"),
        # dcc.Datatable(
        #     id='tabla-estadisticas',
        #     columns=[{"name": col, "id": col} for col in df_estadisticas.columns],
        #     data=df_estadisticas.to_dict('records'),
        #     style_table={'overflowX': 'auto'},
        #     style_cell={'textAlign': 'center', 'padding': '5px'},
        #     style_header={
        #         'backgroundColor': 'rgb(230, 230, 230)',
        #         'fontWeight': 'bold'
        #     },
        #     page_size=10,  # número de filas por página
        #     sort_action='native',  # permite ordenar columnas
        #     filter_action='native'  # permite filtrar por columna
        # )
    ])
