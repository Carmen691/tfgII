from dash import html, dcc

def layout_usuarios(idioma, usuarios):
     return html.Div([
        html.H2("Eliminar usuarios"),

        html.Label("Usuarios:"),
        dcc.Dropdown(
            id='usuarios-dropdown',
            options=[{'label': usu, 'value': usu} for usu in usuarios["usuario"].unique()],
            style={'width': '50%'}
        ),
        html.Button('Eliminar', id='borrar-usuario-button', n_clicks=0),

        html.H2("Añadir usuarios"),
        html.Label("Entidad:"),

        html.Br(),
        html.H4("Principios WCAG:"),
        dcc.Checklist(
            id='principios-checklist',
            options=[
                {"label": "Perceptible", "value": "Perceptible"},
                {"label": "Operable", "value": "Operable"},
                {"label": "Comprensible", "value": "Comprensible"},
                {"label": "Robusto", "value": "Robusto"},
            ],
            value=["Perceptible", "Operable", "Comprensible", "Robusto"],
            labelStyle={'display': 'block'}
        ),

        html.Br(),
        html.H4("Versión WCAG:"),
        dcc.Checklist(
            id='wcag-version-checklist',
            options=[
                {"label": "WCAG 2.0", "value": "2.0"},
                {"label": "WCAG 2.1", "value": "2.1"},
                # {"label": "WCAG 2.2", "value": "2.2"},  # cuando esté disponible
            ],
            value=["2.0", "2.1"],
            labelStyle={'display': 'block'}
        ),

        html.Br(),
        html.H4("Nivel de conformidad:"),
        dcc.Checklist(
            id='nivel-checklist',
            options=[
                {"label": "Nivel A", "value": "A"},
                {"label": "Nivel AA", "value": "AA"},
                {"label": "Nivel AAA", "value": "AAA"},
            ],
            value=["A", "AA", "AAA"],
            labelStyle={'display': 'block'}
        ),

        html.Br(),
        html.H4("Pautas principales:"),
        dcc.Dropdown(
            id='pautas-dropdown',
            multi=True,
            placeholder="Selecciona pautas principales",
            style={'width': '70%'}
        ),

        html.Br(),
        html.H4("Agrupación de datos:"),
        dcc.RadioItems(
            id='agrupacion-radio',
            options=[
                {'label': 'Por versión WCAG', 'value': 'version'},
                {'label': 'Por principio', 'value': 'principio'},
                {'label': 'Por pauta principal', 'value': 'pauta'},
            ],
            value='version',
            labelStyle={'display': 'block'}
        ),

        html.Br(),
        html.H4("Tipo de escala:"),
        dcc.RadioItems(
            id='escala-radio',
            options=[
                {'label': 'Escala 1-5 (Likert)', 'value': 'likert'},
                {'label': 'Escala comprimida (NC / NA / TA)', 'value': 'comprimida'},
            ],
            value='likert',
            labelStyle={'display': 'block'}
        ),
    ])
