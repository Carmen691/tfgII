from dash import html, dcc
import pandas as pd

def layout_importar(idioma, datosEntidades, datosWCAG):
    return html.Div([
        html.H2("Importar nueva auditoría"),
        html.Br(),
        html.Label("Entidad de los datos:"),
        dcc.Store(id='refresh-trigger'),
        dcc.Dropdown(
            id='dropdown-sugerencias',
            options=[{'label': e['nombre'], 'value': e['id']} for e in datosEntidades],
            placeholder='Selecciona...',
            style={'width': '300px'}
        ),
        html.Br(),
        dcc.Input(
        id='input-texto',
        type='text',
        placeholder='Escribe o selecciona...',
        debounce=True,  # Solo dispara el callback cuando el usuario deja de escribir
        style={'width': '300px','marginRight': '10px'}
        ),
        html.Button('Agregar opción', id='add-option-button', n_clicks=0),
        html.Div(id='mensaje-confirmacion'),
        html.Br(),
        html.Label("Versión WCAG"),
        dcc.Dropdown(
            id='dropdown-wcag',
            options=[{'label': row['version'], 'value': row['id']} for _, row in datosWCAG.iterrows()],
            placeholder='Selecciona...',
            style={'width': '300px'}
        ),
        html.Br(),
        html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    html.Div('Arrastra o selecciona un archivo Excel')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',  # Tamaño más pequeño cuando no hay archivo
                    'lineHeight': '60px',  # Centrado vertical
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
            html.Button("Guardar", id="btn-importar", n_clicks=0, style={'marginRight': '10px'}),
            html.Button("Cancelar", id="btn-cancelar", n_clicks=0)
            ], style={
                'display': 'flex',
                'justifyContent': 'flex-end',  # Alinea los botones a la derecha
                'marginTop': '20px'  # Espacio entre el cuadro de arrastre y los botones
            })
        ])
    ])


    