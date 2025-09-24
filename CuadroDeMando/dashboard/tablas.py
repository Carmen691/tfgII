from dash import html
from dash import dash_table, dcc

from dash import html, dash_table, dcc

def layout_datos(df):
    return html.Div([
        dash_table.DataTable(
            id='tabla-datos',  # <--- usamos el id
            editable=True,
            page_action='native',
            page_current=0,
            page_size=10,
            data=df.to_dict('records'),
            columns=[
                {"name": "Criterios", "id": "Criterios"},
                {"name": "Entidades", "id": "Entidades"},
                {"name": "Valores", "id": "Valores", "presentation": "dropdown", "editable": True},
            ],
            dropdown={
                "Valores": {
                    "options": [
                        {"label": "No conseguido", "value": "No conseguido"},
                        {"label": "Parcialmente conseguido", "value": "Parcialmente conseguido"},
                        {"label": "No aplicable", "value": "No aplicable"},
                        {"label": "Ampliadamente conseguido", "value": "Ampliadamente conseguido"},
                        {"label": "Totalmente conseguido", "value": "Totalmente conseguido"},
                    ]
                }
            },
            css=[{
                "selector": "#tabla-datos .dash-dropdown",
                "rule": "position: relative !important; z-index: 9999 !important; min-width: 180px !important;"
            }]
        )
    ])
