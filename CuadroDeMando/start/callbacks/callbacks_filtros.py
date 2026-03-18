from dash import Output, Input, State, ctx
import dash
import pandas as pd
import data.querys as qr

def registrar_callbacks_filtros(app, data):

    @app.callback(
        Output('tipo-entidad-dropdown', 'value'),
        Output('entidad-dropdown', 'options'),
        Output('entidad-dropdown', 'value'),
        Input('url', 'pathname'),                
        Input('tipo-entidad-dropdown', 'value'),  
        State('store-tipo-entidad', 'data'),
        State('entidad-store', 'data')
    )
    def inicializar_o_actualizar_dropdowns(pathname, tipo_cambiado, store_tipo, store_entidades):
        if pathname != "/dash/filtros":
            raise dash.exceptions.PreventUpdate
        
        if store_tipo:
            tipo_seleccionado = store_tipo  
        elif tipo_cambiado:
            tipo_seleccionado = tipo_cambiado  
        else:
            tipos = qr.obtener_tipos_entidad()
            tipo_seleccionado = tipos[0][1]

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

    # --- Guardar filtros al pulsar el botón ---
    @app.callback(
        Output('entidad-store', 'data'),
        Output('store-tipo-entidad', 'data'),
        Input('boton-actualizar', 'n_clicks'),
        State('tipo-entidad-dropdown', 'value'),
        State('entidad-dropdown', 'value'),
        prevent_initial_call=True
    )
    def guardar_filtros(n_clicks, tipo, entidades):
        if not n_clicks:
            raise dash.exceptions.PreventUpdate
        return entidades, tipo