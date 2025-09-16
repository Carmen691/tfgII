from dash import html, dcc
import dash_bootstrap_components as dbc


def layout_filtros(idioma, tiposEntidad, entidades):    
    return html.Div([
        html.Label("Tipo entidad:"),
        dcc.Dropdown(
            id='tipo-entidad-dropdown',
            options=[{'label': cat, 'value': cat} for cat in tiposEntidad["nombre"].unique()],
            multi=False,
            value=tiposEntidad["nombre"].unique()[0],
            style={'width': '100%'}
        ),
        html.Br(),
        html.Label("Entidad:"),
        dcc.Dropdown(
            id='entidad-dropdown',
            options=[{'label': cat, 'value': cat} for cat in entidades["nombre"].unique()],
            multi=True,
            value=list(entidades),
            style={'width': '100%'}
        ),

    #     html.Br(),
    #     html.H4("Principios WCAG:"),
    #     dcc.Checklist(
    #         id='principios-checklist',
    #         options=[
    #             {"label": "Perceptible", "value": "Perceptible"},
    #             {"label": "Operable", "value": "Operable"},
    #             {"label": "Comprensible", "value": "Comprensible"},
    #             {"label": "Robusto", "value": "Robusto"},
    #         ],
    #         value=["Perceptible", "Operable", "Comprensible", "Robusto"],
    #         labelStyle={'display': 'block'}
    #     ),

    #     html.Br(),
    #     html.H4("Versión WCAG:"),
    #     dcc.Checklist(
    #         id='wcag-version-checklist',
    #         options=[
    #             {"label": "WCAG 2.0", "value": "2.0"},
    #             {"label": "WCAG 2.1", "value": "2.1"},
    #         ],
    #         value=["2.0", "2.1"],
    #         labelStyle={'display': 'block'}
    #     ),
    # ], style={'width': '48%', 'padding': '10px'})

    # columna2 = html.Div([
    #     html.H4("Nivel de conformidad:"),
    #     dcc.Checklist(
    #         id='nivel-checklist',
    #         options=[
    #             {"label": "Nivel A", "value": "A"},
    #             {"label": "Nivel AA", "value": "AA"},
    #             {"label": "Nivel AAA", "value": "AAA"},
    #         ],
    #         value=["A", "AA", "AAA"],
    #         labelStyle={'display': 'block'}
    #     ),

    #     html.Br(),
    #     html.H4("Agrupación de datos:"),
    #     dcc.RadioItems(
    #         id='agrupacion-radio',
    #         options=[
    #             {'label': 'Por versión WCAG', 'value': 'version'},
    #             {'label': 'Por principio', 'value': 'principio'},
    #             {'label': 'Por pauta principal', 'value': 'pauta'},
    #         ],
    #         value='version',
    #         labelStyle={'display': 'block'}
    #     ),

    #     html.Br(),
    #     html.H4("Tipo de escala:"),
    #     dcc.RadioItems(
    #         id='escala-radio',
    #         options=[
    #             {'label': 'Escala 1-5 (Likert)', 'value': 'likert'},
    #             {'label': 'Escala comprimida (NC / NA / TA)', 'value': 'comprimida'},
    #         ],
    #         value='likert',
    #         labelStyle={'display': 'block'}
    #     ),
        html.Br(),
        html.Button("Actualizar", id="boton-actualizar", n_clicks=0),

    ], style={'width': '48%', 'padding': '10px'})

    # return html.Div([
    #     html.H2("Filtros"),
    #     html.Div([columna1], style={'display': 'flex', 'justify-content': 'space-between'}),

    #])
