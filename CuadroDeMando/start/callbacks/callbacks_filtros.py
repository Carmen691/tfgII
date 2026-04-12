from dash import Output, Input, State, ctx
import dash
from dash.exceptions import PreventUpdate
import pandas as pd
import data.querys as qr

def registrar_callbacks_filtros(app):

    @app.callback(
        Output('tipo-entidad-dropdown', 'value'),
        Output('entidad-dropdown', 'options'),
        Output('entidad-dropdown', 'value'),
        Input('init-done', 'data'),
        Input('url', 'pathname'),                
        Input('tipo-entidad-dropdown', 'value'),  
        State('store-tipo-entidad', 'data'),
        State('entidad-store', 'data')
    )
    def inicializar_o_actualizar_dropdowns(cargar, pathname, tipo_cambiado, store_tipo, store_entidades):
        if not cargar or  pathname != "/dash/filtros":
            raise dash.exceptions.PreventUpdate
        
        if store_tipo:
            tipo_seleccionado = store_tipo  
        elif tipo_cambiado:
            tipo_seleccionado = tipo_cambiado  
        else:
            tipos = qr.obtener_tipos_entidad()
            tipo_seleccionado = tipos[0][0]

        df_entidades = pd.DataFrame(
            qr.obtener_entidades_por_nombre(tipo_seleccionado),
            columns=["id", "nombre", "id_tipo"]
        )
        nombres = df_entidades["nombre"].unique().tolist()
        options = [{'label': n, 'value': n} for n in nombres]

        if store_entidades and tipo_cambiado is None:
            seleccion = [v for v in store_entidades if v in nombres]
            valor_entidades = seleccion if seleccion else nombres
        else:
            valor_entidades = nombres

        return tipo_seleccionado, options, valor_entidades


    @app.callback(
        Output('entidad-store', 'data', allow_duplicate=True),
        Output('store-tipo-entidad', 'data', allow_duplicate=True),
        Input('tipo-entidad-dropdown', 'value'),
        Input('entidad-dropdown', 'value'),
        State('entidad-store', 'data'),
        State('store-tipo-entidad', 'data'),
        prevent_initial_call='initial_duplicate'
    )
    def init_filtros(tipo, entidades, entidades_store, tipo_store):

        if entidades_store is None and tipo_store is None:
            return entidades, tipo

        raise PreventUpdate
    
    # @app.callback(
    #     Output('entidad-store', 'data', allow_duplicate=True),
    #     Output('store-tipo-entidad', 'data', allow_duplicate=True),
    #     Input('init-trigger', 'n_intervals'),
    #     State('entidad-store', 'data'),
    #     State('store-tipo-entidad', 'data'),
    #     prevent_initial_call='initial_duplicate'
    # )
    # def init_filtros(n, entidades_store, tipo_store):
    #     if entidades_store is None and tipo_store is None:
    #         return [], None
    #     raise PreventUpdate
    
    @app.callback(
        Output('entidad-store', 'data'),
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
        return entidades, tipo, principios, versiones, niveles

    # @app.callback(
    #     Output('entidad-store', 'data'),
    #     Output('store-tipo-entidad', 'data'),
    #     Input('init-trigger', 'n_intervals'),
    #     Input('boton-actualizar', 'n_clicks'),
    #     State('tipo-entidad-dropdown', 'value'),
    #     State('entidad-dropdown', 'value'),
    #     State('entidad-store', 'data'),
    #     State('store-tipo-entidad', 'data'),
    # )
    # def guardar_filtros(n_init, n_clicks, tipo, entidades, entidades_store, tipo_store):

    #     trigger = ctx.triggered_id

    #     if trigger == 'init-trigger' and not entidades_store and not tipo_store:
    #         return entidades, tipo

    #     if trigger == 'boton-actualizar':
    #         return entidades, tipo

    #     raise PreventUpdate