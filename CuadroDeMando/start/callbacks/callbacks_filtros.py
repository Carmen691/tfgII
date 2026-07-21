from dash import Output, Input, State, ctx, dcc, html, no_update
import dash
from dash.exceptions import PreventUpdate
import pandas as pd
import data.querys as qr
import dash_mantine_components as dmc
from collections import defaultdict



def registrar_callbacks_filtros(app):

    @app.callback(
        Output("tipo-entidad-dropdown", "data"),
        Output("tipo-entidad-dropdown", "value"),
        Input('url', 'pathname'),
        State("store-tipo-entidad", "data"),
    )
    def cargar_tipos_entidad(pathname, tipo_guardado):
        if pathname != "/dash/filtros":
            return dash.no_update, dash.no_update

        tipos = pd.DataFrame(qr.obtener_tipos_entidad()).to_dict('records')

        options = [
            {
                "label": t["nombre"],
                "value": str(t["id"])
            }
            for t in tipos
        ]

        # Si había uno guardado y sigue existiendo, lo usamos
        ids = [str(t["id"]) for t in tipos]

        if tipo_guardado is not None and str(tipo_guardado) in ids:
            value = str(tipo_guardado)
        elif ids:
            value = ids[0]
        else:
            value = None

        return options, value


    @app.callback(
        Output('entidad-dropdown', 'data'),
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

        # =====================================================
        # OPCIONES AGRUPADAS POR LETRA
        # =====================================================

        grupos = defaultdict(list)

        df_entidades = df_entidades.sort_values("nombre")

        for _, row in df_entidades.iterrows():

            letra = row["nombre"][0].upper()

            grupos[letra].append(
                {
                    "label": row["nombre"],
                    "value": str(row["id"])
                }
            )

        options = [

            {
                "group": letra,
                "items": items
            }

            for letra, items in grupos.items()

        ]

        # =====================================================
        # VALORES SELECCIONADOS
        # =====================================================

        ids_validos = [str(i) for i in df_entidades["id"].tolist()]

        if store_entidades and tipo_cambiado == store_tipo:

            seleccion = [
                v for v in store_entidades
                if v in ids_validos
            ]

            valor_entidades = seleccion if seleccion else ids_validos

        else:

            valor_entidades = ids_validos

        return options, valor_entidades


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

    
    @app.callback(
        Output('store-entidad', 'data'),
        Output('store-tipo-entidad', 'data'),
        Output('store-principios', 'data'),
        Output('store-versiones', 'data'),
        Output('store-niveles', 'data'),
        Output('store-fecha', 'data'),
        Output("mensaje-filtros", "children"),
        Output("mensaje-filtros", "style"),
        Input('boton-actualizar', 'n_clicks'),
        State('tipo-entidad-dropdown', 'value'),
        State('entidad-dropdown', 'value'),
        State('principios-checklist', 'value'),
        State('wcag-version-checklist', 'value'),
        State('nivel-checklist', 'value'),
        State('version-auditoria-dropdown', 'value'),
        State("store-idioma", "data"),
        prevent_initial_call=True
    )
    def actualizar_filtros(n, tipo, entidades, principios, versiones, niveles, fecha, idioma):
        if n > 0:
            textos = qr.obtener_textos_seccion(idioma, "filtros")
            return entidades, tipo, principios, versiones, niveles, fecha, textos["filtros_seleccionados"], {"color": "green"}
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    @app.callback(
        Output("principios-checklist", "children", allow_duplicate=True),
        Output("wcag-version-checklist", "children"),
        Output("nivel-checklist", "children"),
        Input("principios-checklist", "value"),
        Input("wcag-version-checklist", "value"),
        Input("nivel-checklist", "value"),
        prevent_initial_call=True
    )
    def actualizar_filtros_dependientes(principios_sel, wcag_sel, nivel_sel):

        principios_sel = principios_sel or []
        wcag_sel = wcag_sel or []
        nivel_sel = nivel_sel or []

        df = pd.DataFrame(qr.obtener_opciones_filtros())

        niveles = pd.DataFrame(qr.obtener_niveles()).to_dict("records")
        wcag = pd.DataFrame(qr.obtener_tipos_wcag()).to_dict("records")
        principios = pd.DataFrame(qr.obtener_principios()).to_dict("records")

        # Convertimos a string para que coincida con Mantine
        df["id_principio"] = df["id_principio"].astype(str)
        df["id_version"] = df["id_version"].astype(str)
        df["id_nivel"] = df["id_nivel"].astype(str)

        # =====================================================
        # PRINCIPIOS DISPONIBLES
        # =====================================================

        df_principios = df.copy()

        if wcag_sel:
            df_principios = df_principios[
                df_principios["id_version"].isin(wcag_sel)
            ]

        if nivel_sel:
            df_principios = df_principios[
                df_principios["id_nivel"].isin(nivel_sel)
            ]

        ok_principios = set(df_principios["id_principio"])

        # =====================================================
        # VERSIONES DISPONIBLES
        # =====================================================

        df_wcag = df.copy()

        if principios_sel:
            df_wcag = df_wcag[
                df_wcag["id_principio"].isin(principios_sel)
            ]

        if nivel_sel:
            df_wcag = df_wcag[
                df_wcag["id_nivel"].isin(nivel_sel)
            ]

        ok_wcag = set(df_wcag["id_version"])

        # =====================================================
        # NIVELES DISPONIBLES
        # =====================================================

        df_niveles = df.copy()

        if principios_sel:
            df_niveles = df_niveles[
                df_niveles["id_principio"].isin(principios_sel)
            ]

        if wcag_sel:
            df_niveles = df_niveles[
                df_niveles["id_version"].isin(wcag_sel)
            ]

        ok_niveles = set(df_niveles["id_nivel"])

        # =====================================================
        # COMPONENTES
        # =====================================================

        principios_children = [

            dmc.Checkbox(
                label=p["nombre"],
                value=str(p["id"]),
                disabled=str(p["id"]) not in ok_principios,
                size="md",
                radius="xl",
                color="blue",
                className="checkbox-item",
            )

            for p in principios

        ]

        wcag_children = [

            dmc.Checkbox(
                label=w["version"],
                value=str(w["id"]),
                disabled=str(w["id"]) not in ok_wcag,
                size="md",
                radius="xl",
                color="blue",
                className="checkbox-item",
            )

            for w in wcag

        ]

        niveles_children = [

            dmc.Checkbox(
                label=n["nombre"],
                value=str(n["id"]),
                disabled=str(n["id"]) not in ok_niveles,
                size="md",
                radius="xl",
                color="blue",
                className="checkbox-item",
            )

            for n in niveles

        ]

        return (
            principios_children,
            wcag_children,
            niveles_children,
        )

    @app.callback(
        Output("version-auditoria-dropdown", "data"),
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
                "value": str(row["id"])
            }
            for _, row in versiones.iterrows()
        ]

        return opciones, opciones[0]["value"]
    
    @app.callback(
        Output("tipo_entidad", "children"),
        Output("tipo-entidad-dropdown", "placeholder"),
        Output("fecha_wcag", "children"),
        Output("escala_visualizacion", "children"),
        Output("entidades", "children"),
        Output("principios_wcag", "children"),
        Output("version_wcag", "children"),
        Output("nivel", "children"),
        Output("boton-actualizar", "children"),
        Output("txt-deseleccionar", "children"),
        Output("txt-seleccionar-todas", "children"),
        Output("titulo-filtros", "children"),
        Input("store-idioma", "data")
    )
    def textos_gestion(idioma):

        filtros = qr.obtener_textos_seccion(idioma, "filtros")
        usuarios = qr.obtener_textos_seccion(idioma, "usuarios")
        auditorias = qr.obtener_textos_seccion(idioma, "auditorias")

        return (
            filtros["tipo_entidad"],
            usuarios["seleccionar"],
            auditorias["fecha"],
            filtros["escala_visualizacion"],
            filtros["entidades"],
            filtros["principios"],
            filtros["version"],
            filtros["nivel"],
            filtros["actualizar"],
            filtros["deseleccionar"],
            filtros["seleccionar_todo"],
            filtros["titulo_filtros"]
        )


    @app.callback(
        Output("entidad-dropdown", "value"),
        Input("btn-seleccionar-todas", "n_clicks"),
        Input("btn-deseleccionar", "n_clicks"),
        Input("txt-seleccionar-todas", "n_clicks"),
        Input("txt-deseleccionar", "n_clicks"),
        State("entidad-dropdown", "data"),
        prevent_initial_call=True,
    )
    def acciones_entidades(
        btn_sel,
        btn_des,
        txt_sel,
        txt_des,
        data,
    ):

        trigger = ctx.triggered_id

        if trigger in ("btn-deseleccionar", "txt-deseleccionar"):
            return []

        if trigger in ("btn-seleccionar-todas", "txt-seleccionar-todas"):

            seleccion = []

            for grupo in data:
                for item in grupo["items"]:
                    seleccion.append(item["value"])

            return seleccion

        raise PreventUpdate
        

    @app.callback(
        Output("principios-checklist", "options"),
        Output("principios-checklist", "value"),
        Input("url", "pathname"),
        State("store-principios", "data"),
    )
    def cargar_principios(pathname, principios_guardados):

        if pathname != "/dash/filtros":
            return dash.no_update, dash.no_update

        principios = pd.DataFrame(qr.obtener_principios()).to_dict("records")

        options = [
            {"label": p["nombre"], "value": str(p["id"])}
            for p in principios
        ]

        ids = [str(p["id"]) for p in principios]

        if principios_guardados:
            value = [v for v in map(str, principios_guardados) if v in ids]
            if not value:
                value = ids
        else:
            value = ids

        return options, value
    

    @app.callback(
        Output("wcag-version-checklist", "options"),
        Output("wcag-version-checklist", "value"),
        Input("url", "pathname"),
        State("store-versiones", "data"),
    )
    def cargar_versiones(pathname, versiones_guardadas):

        if pathname != "/dash/filtros":
            return dash.no_update, dash.no_update

        versiones = pd.DataFrame(qr.obtener_versiones()).to_dict("records")

        options = [
            {
                "label": v["version"],
                "value": str(v["id"])
            }
            for v in versiones
        ]

        ids = [str(v["id"]) for v in versiones]

        if versiones_guardadas:
            value = [v for v in map(str, versiones_guardadas) if v in ids]
            if not value:
                value = ids
        else:
            value = ids

        return options, value


    @app.callback(
        Output("nivel-checklist", "options"),
        Output("nivel-checklist", "value"),
        Input("url", "pathname"),
        State("store-niveles", "data"),
    )
    def cargar_niveles(pathname, niveles_guardados):

        if pathname != "/dash/filtros":
            return dash.no_update, dash.no_update

        niveles = pd.DataFrame(qr.obtener_niveles()).to_dict("records")

        options = [
            {
                "label": n["nombre"],
                "value": str(n["id"])
            }
            for n in niveles
        ]

        ids = [str(n["id"]) for n in niveles]

        if niveles_guardados:
            value = [v for v in map(str, niveles_guardados) if v in ids]
            if not value:
                value = ids
        else:
            value = ids

        return options, value
    

    @app.callback(
        Output("div-escala-visualizacion", "style"),
        Input("tipo-entidad-dropdown", "value")
    )
    def mostrar_escala(tipo_entidad):

        escala = qr.obtener_escala_tipo_auditoria(tipo_entidad)[0][0]

        if escala == 1:   # Likert 5
            return {}

        return {"display": "none"}
    

    @app.callback(
        Output("escala-visualizacion-dropdown", "data"),
        Output("escala-visualizacion-dropdown", "value"),
        Input('url', 'pathname')
    )
    def dropdown_escala_filtros(pathname):
        if pathname != "/dash/filtros":
            raise PreventUpdate

        escalas = pd.DataFrame(qr.obtener_escalas())

        opciones_escala = [
            {"label": row["descripcion"], "value": str(row["id"])}
            for _, row in escalas.iterrows()
        ]

        # Seleccionar la primera opción por defecto
        valor = opciones_escala[0]["value"] if opciones_escala else None

        return opciones_escala, valor