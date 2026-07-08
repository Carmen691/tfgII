from dash import Output, Input, State, ctx, dcc, html, no_update
import dash
from dash.exceptions import PreventUpdate
import pandas as pd
import data.querys as qr

def registrar_callbacks_filtros(app):

    @app.callback(
        Output("tipo-entidad-dropdown", "options"),
        Output("tipo-entidad-dropdown", "value"),
        Input('url', 'pathname'),
        State("store-tipo-entidad", "data"),
    )
    def cargar_tipos_entidad(pathname, tipo_guardado):
        if pathname != "/dash/filtros":
            raise PreventUpdate

        tipos = pd.DataFrame(qr.obtener_tipos_entidad()).to_dict('records')

        options = [
            {
                "label": t["nombre"],
                "value": t["id"]
            }
            for t in tipos
        ]

        # Si había uno guardado y sigue existiendo, lo usamos
        ids = [t["id"] for t in tipos]

        if tipo_guardado in ids:
            value = tipo_guardado
        elif ids:
            value = ids[0]
        else:
            value = None

        return options, value

    @app.callback(
        Output('entidad-dropdown', 'options'),
        Output('entidad-dropdown', 'value'),
        Input('url', 'pathname'),                
        Input('tipo-entidad-dropdown', 'value'),  
        State('store-tipo-entidad', 'data'),
        State('store-entidad', 'data')
    )
    def inicializar_o_actualizar_dropdowns(pathname, tipo_cambiado, store_tipo, store_entidades):
        if pathname != "/dash/filtros":
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
            columns=["id", "nombre", "id_version"]
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


    # @app.callback(
    #     Output('tipo-entidad-dropdown', 'value'),
    #     Input('store-tipo-entidad', 'data'),
    #     State('tipo-entidad-dropdown', 'value'),
    #     prevent_initial_call=True
    # )
    # def cargar_dropdown(tipoEntidad, valor_actual):
    #     if valor_actual is not None:
    #         return no_update

    #     return tipoEntidad

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
        Output('store-fecha', 'data'),
        Input('boton-actualizar', 'n_clicks'),
        State('tipo-entidad-dropdown', 'value'),
        State('entidad-dropdown', 'value'),
        State('principios-checklist', 'value'),
        State('wcag-version-checklist', 'value'),
        State('nivel-checklist', 'value'),
        State('version-auditoria-dropdown', 'value'),
        prevent_initial_call=True
    )
    def actualizar_filtros(n, tipo, entidades, principios, versiones, niveles, fecha):
        if n > 0:
            return entidades, tipo, principios, versiones, niveles, fecha
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    @app.callback(
        Output("principios-checklist", "options"),
        Output("wcag-version-checklist", "options"),
        Output("nivel-checklist", "options"),
        Input("principios-checklist", "value"),
        Input("wcag-version-checklist", "value"),
        Input("nivel-checklist", "value")
    )
    def actualizar_filtros_dependientes(principios_sel, wcag_sel, nivel_sel):
        df = pd.DataFrame(qr.obtener_opciones_filtros())

        niveles = pd.DataFrame(qr.obtener_niveles()).to_dict("records")
        wcag = pd.DataFrame(qr.obtener_tipos_wcag()).to_dict("records")
        principios = pd.DataFrame(qr.obtener_principios()).to_dict("records")

        # Aplicamos los filtros seleccionados
        df_principios = df.copy()
        if wcag_sel:
            df_principios = df_principios[df_principios["id_version"].isin(wcag_sel)]

        if nivel_sel:
            df_principios = df_principios[df_principios["id_nivel"].isin(nivel_sel)]

        ok_principios = set(df_principios["id_principio"])

        df_wcag = df.copy()

        if principios_sel:
            df_wcag = df_wcag[df_wcag["id_principio"].isin(principios_sel)]

        if nivel_sel:
            df_wcag = df_wcag[df_wcag["id_nivel"].isin(nivel_sel)]

        ok_wcag = set(df_wcag["id_version"])

        df_niveles = df.copy()

        if principios_sel:
            df_niveles = df_niveles[df_niveles["id_principio"].isin(principios_sel)]

        if wcag_sel:
            df_niveles = df_niveles[df_niveles["id_version"].isin(wcag_sel)]

        ok_niveles = set(df_niveles["id_nivel"])

        principios_options = [
            {
                "label": p["nombre"],
                "value": p["id"],
                "disabled": p["id"] not in ok_principios
            }
            for p in principios
        ]

        wcag_options = [
            {
                "label": w["version"],
                "value": w["id"],
                "disabled": w["id"] not in ok_wcag
            }
            for w in wcag
        ]

        niveles_options = [
            {
                "label": n["nombre"],
                "value": n["id"],
                "disabled": n["id"] not in ok_niveles
            }
            for n in niveles
        ]

        return (
            principios_options,
            wcag_options,
            niveles_options
        )

    @app.callback(
        Output("version-auditoria-dropdown", "options"),
        Output("version-auditoria-dropdown", "value"),
        Input("tipo-entidad-dropdown", "value")
    )
    def cargar_versiones_auditoria(id_tipo):

        if not id_tipo:
            return [], None

        versiones = pd.DataFrame(
            qr.obtener_versiones_auditoria(id_tipo),
            columns=["id", "fecha"]
        )

        if versiones.empty:
            return [], None

        opciones = [
            {
                "label": row["fecha"].strftime("%d/%m/%Y"),
                "value": row["id"]
            }
            for _, row in versiones.iterrows()
        ]

        return opciones, opciones[0]["value"]
    

    @app.callback(
        Output("tipo_entidad", "children"),
        Output("tipo-entidad-dropdown", "placeholder"),
        Output("fecha_wcag", "children"),
        Output("entidades", "children"),
        Output("principios_wcag", "children"),
        Output("version_wcag", "children"),
        Output("nivel", "children"),
        Output("boton-actualizar", "children"),
        Input("store-idioma", "data")
    )
    def textos_gestion(idioma):

        return (
            qr.obtener_textos_interfaz(idioma, "filtros", "tipo_entidad"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "seleccionar"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "fecha"),
            qr.obtener_textos_interfaz(idioma, "filtros", "entidades"),
            qr.obtener_textos_interfaz(idioma, "filtros", "principios"),
            qr.obtener_textos_interfaz(idioma, "filtros", "version"),
            qr.obtener_textos_interfaz(idioma, "filtros", "nivel"),
            qr.obtener_textos_interfaz(idioma, "filtros", "actualizar")
        )
