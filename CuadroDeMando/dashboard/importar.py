from dash import html, dcc

def layout_importar():
    return dcc.Loading(
        id="loading-importar",
        type="circle",
        fullscreen=False,
        children=html.Div([

            html.H2(id="importar-titulo"),

            html.Br(),

            html.Label(id="entidad-datos"),

            dcc.Dropdown(
                id='dropdown-sugerencias',
                style={'width': '300px'}
            ),

            dcc.Store(id='refresh-trigger'),

            html.Br(),

            dcc.Input(
                id='input-texto',
                type='text',
                debounce=True,
                style={'width': '300px', 'marginRight': '10px'}
            ),

            html.Button(id='add-option-button', n_clicks=0),

            html.Div(id='mensaje-confirmacion'),

            html.Br(),

            html.Label(id="version-wcag"),

            dcc.Dropdown(
                id='dropdown-wcag',
                style={'width': '300px'}
            ),

            html.Br(),

            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    html.Div(id="arrastra-ficheros")
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '2px',
                    'borderStyle': 'dashed',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'cursor': 'pointer',
                    'padding': '10px'
                },
                multiple=False,
                accept='.xlsx,.xls',
            ),

            html.Div(id='file-upload-info'),

            html.Div([
                html.Button(id="btn-importar", n_clicks=0, className="btn-success")
            ], className="fila-botones"),


            html.Div(
                id="mensaje-importacion",
                className="mensaje"
            )

        ])
    )