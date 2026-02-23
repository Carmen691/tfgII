from dash import html, dcc

def layout_graficos(fig, figPorcentaje, figMapaCalor):
    return html.Div([
        dcc.Graph(id='grafico-general', figure=fig),
        dcc.Graph(id='grafico-porcentaje', figure=figPorcentaje),
        dcc.Graph(id='grafico-mapa-calor', figure=figMapaCalor),

        html.Div(
            children=[
                html.H4("Estadísticas WCAG", style={"margin-bottom": "10px"}),
                html.P("Total Entidades: 25"),
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
        )
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
