from dash import dash_table, html, dcc
def layout_datos():

    return dcc.Loading(
        id="loading-datos",
        type="circle",
        fullscreen=False,
        children=html.Div([

            dash_table.DataTable(
                id='tabla-datos',
                editable=True,
                page_action='native',
                page_current=0,
                page_size=10,
                data=[],
                columns=[]
            ),

            html.Button(
                id="btn-guardar-tabla",
                n_clicks=0
            ),

            html.Div(id="mensaje-guardar")
        ])
    )