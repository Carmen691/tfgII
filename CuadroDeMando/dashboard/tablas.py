from dash import html
from dash import dash_table, dcc

def layout_datos(df):
    return html.Div([
        # dcc.Store(id="store-refresh-trigger"),
        # dcc.Store(id='store-datos', data=df.to_dict('records')),
        # dcc.Store(id='store-celda-seleccionada'),

        dash_table.DataTable(
            id='tabla-datos',
            editable=True,
            #page_action='custom',
            page_action='native',
            page_current=0,
            page_size=10,
            data=df.to_dict('records'),
            #style_table={"overflowX": "auto"},
            columns=[
                {"name": "Criterios", "id": "Criterios"},
                {"name": "Entidades", "id": "Entidades"},
                {
                    "name": "Valores",
                    "id": "Valores",
                    "presentation": "dropdown",
                    "editable" : True
                },
            ],
            dropdown={
                "Valores": {
                    "options": [
                        {"label": "No conseguido", "value": "No conseguido"},
                        {"label": "Parcialmente conseguido", "value": "Parcialmente conseguido"},
                        {"label": "No aplicable", "value": "No aplicable"},
                        {"label": "Ampliamente conseguido", "value": "Ampliamente conseguido"},
                        {"label": "Totalmente conseguido", "value": "Totalmente conseguido"},
                    ]
                }
            },
            style_table={"overflowX": "visible"},
            style_cell={"overflow": "visible"},
                css=[{
                    "selector": ".dash-spreadsheet-container .dash-dropdown",
                    "rule": "position: relative !important; z-index: 10000 !important;"
                }]
        )
    ], style={"overflow": "visible", "position": "relative", "zIndex": 1000})
