from dash import html
from dash import dash_table, dcc

def layout_datos(df, dropdown_opciones):
    return html.Div([
    dcc.Store(id="store-refresh-trigger"),
    dcc.Store(id='store-datos', data=df.to_dict('records')),
    dcc.Store(id='store-celda-seleccionada'),  # para guardar coordenadas celda
    html.Div(id="dropdown-celda"),
    dash_table.DataTable(
        id='tabla-datos',
        columns=[
            {
                "name": col,
                "id": col,
                "editable": (col == "Valores"),
                "presentation": "dropdown" if col == "Valores" else "input"
            } for col in df.columns
        ],
        data=df.iloc[:10].to_dict('records'),
        editable=True,
        dropdown_conditional=[
            {
                'if': {
                    'column_id': 'Valores'
                },
                'options': dropdown_opciones
            }
        ],
        page_action='custom',
        page_current=0,
        page_size=10,
        style_table={"overflowX": "auto"},
    )
    ])

