from dash import html
from dash import dash_table

def layout_datos(df):
    return html.Div([
        html.H2("Tabla de Datos"),
        dash_table.DataTable(
            id='tabla-datos',
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.iloc[:10].to_dict('records'),
            style_table={'height': '400px', 'overflowY': 'auto', 'overflowX': 'auto'},
            style_cell={'textAlign': 'center', 'minWidth': '150px', 'width': '150px', 'maxWidth': '200px'},
            style_header={'fontWeight': 'bold', 'backgroundColor': 'lightgrey'},
            page_size=10,
            page_action='custom',
            page_current=0,
        )
    ])
