# dashboard/layout.py
from dash import html, dcc, dash_table


def crear_layout(df, idioma, entidades, fig):
    return html.Div([
        # Menú lateral
        html.Div([
            html.H2("Menu", style={"color": "white", "padding": "10px"}),
            dcc.Link("Dashboard", href="/dash/", style={"display": "block", "padding": "10px", "color": "white"}),
            dcc.Link("Opcion 1", href="#", style={"display": "block", "padding": "10px", "color": "white"}),
            dcc.Link("Cerrar sesion", href="/logout", style={"display": "block", "padding": "10px", "color": "white"}),
            html.A("Cerrar sesion", href="/logout", target="_self", className="nav-link")
        ], style={
            "position": "fixed",
            "top": "0",
            "left": "0",
            "width": "250px",
            "height": "100%",
            "backgroundColor": "#2c3e50",
            "paddingTop": "20px",
            "zIndex": "1000"
        }),

        # Contenido principal (con padding para que no lo tape el menú)
        html.Div([
            html.H1("Dashboard", style={"paddingTop": "20px"}),
            
            # Dropdowns
            html.Label("Idioma:"),
            dcc.Dropdown(
                id='idioma-dropdown',
                options=[{'label': cat, 'value': cat} for cat in idioma["nombre"].unique()],
                value="Espanol",
                style={'width': '50%'}
            ),
            
            html.Label("Entidad:"),
            dcc.Dropdown(
                id='entidad-dropdown',
                options=[{'label': cat, 'value': cat} for cat in entidades["nombre"].unique()],
                multi=True,
                style={'width': '50%'}
            ),

            dcc.Graph(id="grafico", figure=fig),
            # Tabla con los datos
        dash_table.DataTable(
        id='tabla-datos',
        columns=[{"name": col, "id": col} for col in df.columns],
        #data=df.to_dict('records'),
        data=df.iloc[:10].to_dict('records'),
        # Estilo de la tabla
        style_table={'height': '400px', 'overflowY': 'auto', 'overflowX': 'auto'},  # Scroll vertical y horizontal
        style_cell={'textAlign': 'center', 'minWidth': '150px', 'width': '150px', 'maxWidth': '200px'},  # Ajustar tamaño de celdas
        style_header={'fontWeight': 'bold', 'backgroundColor': 'lightgrey'},  # Estilo del encabezado
        
        # Paginación
        page_size=10,  # Número de filas por página
        page_action='custom',  # Activar paginación
        page_current=0,),
        ], style={"marginLeft": "260px", "padding": "20px"})  # Esto evita que se solape con el menú lateral
    ])
