from dash import Output, Input, State, ctx, dcc, html, no_update
import dash
from dash.exceptions import PreventUpdate
import pandas as pd
import data.querys as qr

def registrar_callbacks_filtros(app):

    @app.callback(
        Output('entidad-dropdown', 'options'),
        Output('entidad-dropdown', 'value'),
        Input('init-done', 'data'),
        Input('url', 'pathname'),                
        Input('tipo-entidad-dropdown', 'value'),  
        State('store-tipo-entidad', 'data'),
        State('store-entidad', 'data')
    )
    def inicializar_o_actualizar_dropdowns(cargar, pathname, tipo_cambiado, store_tipo, store_entidades):
        if not cargar or pathname != "/dash/filtros":
            raise dash.exceptions.PreventUpdate

        if store_tipo == tipo_cambiado and store_tipo is not None:
            tipo_seleccionado = store_tipo
        elif store_tipo != tipo_cambiado and tipo_cambiado is not None:
            tipo_seleccionado = tipo_cambiado
        else:
            tipos = qr.obtener_tipos_entidad()
            tipo_seleccionado = tipos[0][0]

        df_entidades = pd.DataFrame(
            qr.obtener_entidades_por_nombre(tipo_seleccionado),
            columns=["id", "nombre", "id_tipo"]
        )

        options = [
            {"label": row["nombre"], "value": row["id"]}
            for _, row in df_entidades.iterrows()
        ]

        ids_validos = df_entidades["id"].tolist()

        if store_entidades and tipo_cambiado == store_tipo:
            seleccion = [v for v in store_entidades if v in ids_validos]
            valor_entidades = seleccion if seleccion else ids_validos
        else:
            valor_entidades = ids_validos

        return options, valor_entidades


    @app.callback(
        Output('tipo-entidad-dropdown', 'value'),
        Input('store-tipo-entidad', 'data'),
        State('tipo-entidad-dropdown', 'value'),
        prevent_initial_call=True
    )
    def cargar_dropdown(tipoEntidad, valor_actual):
        if valor_actual is not None:
            return no_update

        return tipoEntidad

    @app.callback(
        Output('store-entidad', 'data', allow_duplicate=True),
        Input('entidad-dropdown', 'value'),
        State('store-entidad', 'data'),
        prevent_initial_call='initial_duplicate'
    )
    def init_filtros(entidades, entidades_store):

        if entidades_store is None:
            return entidades
        return dash.no_update
    

    @app.callback(
        Output('store-tipo-entidad', 'data', allow_duplicate=True),
        Input('tipo-entidad-dropdown', 'value'),
        State('store-tipo-entidad', 'data'),
        prevent_initial_call='initial_duplicate'
    )
    def init_filtros(tipo, tipo_store):

        if tipo_store is None:
            return tipo
        return dash.no_update

    
    # @app.callback(
    #     Output('store-entidad', 'data', allow_duplicate=True),
    #     Output('store-tipo-entidad', 'data', allow_duplicate=True),
    #     Input('init-trigger', 'n_intervals'),
    #     State('store-entidad', 'data'),
    #     State('store-tipo-entidad', 'data'),
    #     prevent_initial_call='initial_duplicate'
    # )
    # def init_filtros(n, entidades_store, tipo_store):
    #     if entidades_store is None and tipo_store is None:
    #         return [], None
    #     raise PreventUpdate
    
    @app.callback(
        Output('store-entidad', 'data'),
        Output('store-tipo-entidad', 'data'),
        Output('store-principios', 'data'),
        Output('store-versiones', 'data'),
        Output('store-niveles', 'data'),
        Input('boton-actualizar', 'n_clicks'),
        State('tipo-entidad-dropdown', 'value'),
        State('entidad-dropdown', 'value'),
        State('principios-checklist', 'value'),
        State('wcag-version-checklist', 'value'),
        State('nivel-checklist', 'value'),
        prevent_initial_call=True
    )
    def actualizar_filtros(n, tipo, entidades, principios, versiones, niveles):
        if n > 0:
            return entidades, tipo, principios, versiones, niveles
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    @app.callback(
        Output("filtros-container", "children"),
        Input("store-data", "data"),
        State("store-idioma", "data"),
    )
    def cargar_filtros(data, idioma):

        if not data:
            return html.Div("Cargando filtros...")

        tiposEntidad = data["tiposEntidad"]
        entidades = pd.DataFrame(data["entidades"])
        versionesWCAG = pd.DataFrame(data["tiposWCAG"])
        principios = pd.DataFrame(data["principios"])
        niveles = pd.DataFrame(data["niveles"])

        if len(tiposEntidad) == 1 and isinstance(tiposEntidad[0], list):
            tiposEntidad = tiposEntidad[0]

        return html.Div([

            html.H5(
                qr.obtener_textos_interfaz(idioma, "filtros", "filtros"),
                style={"margin-bottom": "20px", "font-weight": "600"}
            ),

            # Tipo entidad
            html.Label(
                qr.obtener_textos_interfaz(idioma, "filtros", "tipo_entidad"),
                className="label-filtro"
            ),

            dcc.Dropdown(
                id='tipo-entidad-dropdown',
                options=[
                    {'label': e['nombre'], 'value': e['id']}
                    for e in tiposEntidad
                ],
                multi=False,
                persistence=True,
                persistence_type='session',
                className="input-style",
            ),

            # Entidad
            html.Label(
                qr.obtener_textos_interfaz(idioma, "filtros", "entidades"),
                className="label-filtro"
            ),

            dcc.Dropdown(
                id='entidad-dropdown',
                options=[
                    {'label': row['nombre'], 'value': row['id']}
                    for _, row in entidades.drop_duplicates('id').iterrows()
                ],
                multi=True,
                persistence=True,
                persistence_type='session',
                className="input-style",
            ),

            # Principios
            html.Div(
                qr.obtener_textos_interfaz(idioma, "filtros", "principios"),
                className="section-title"
            ),

            dcc.Checklist(
                id='principios-checklist',
                options=[
                    {'label': row['nombre'], 'value': row['id']}
                    for _, row in principios.drop_duplicates('id').iterrows()
                ],
                value=principios['id'].drop_duplicates().tolist(),
                className="input-style",
            ),

            # Versión WCAG
            html.Div(
                qr.obtener_textos_interfaz(idioma, "filtros", "version"),
                className="section-title"
            ),

            dcc.Checklist(
                id='wcag-version-checklist',
                options=[
                    {'label': ver, 'value': ver}
                    for ver in versionesWCAG["version"].unique()
                ],
                value=versionesWCAG["version"].unique().tolist(),
                className="input-style",
            ),

            # Nivel
            html.Div(
                qr.obtener_textos_interfaz(idioma, "filtros", "nivel"),
                className="section-title"
            ),

            dcc.Checklist(
                id='nivel-checklist',
                options=[
                    {'label': niv, 'value': niv}
                    for niv in niveles["nombre"].unique()
                ],
                value=niveles['nombre'].drop_duplicates().tolist(),
                className="input-style",
            ),

            html.Button(
                qr.obtener_textos_interfaz(idioma, "filtros", "actualizar"),
                id="boton-actualizar",
                n_clicks=0,
                className="btn-actualizar"
            )
        ])