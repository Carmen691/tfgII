import dash
from dash import Output, Input, State
import pandas as pd
from flask import session
import data.querys as qr


def registrar_callbacks_admin(app):
    @app.callback(
        Output("sidebar", "className"),
        Output("main-content", "className"),
        Output("menu-collapsed", "data"),
        Input("toggle-menu", "n_clicks"),
        State("menu-collapsed", "data"),
        prevent_initial_call=True
    )
    def toggle_menu(n_clicks, is_collapsed):

        collapsed = not is_collapsed

        if collapsed:
            return "sidebar collapsed", "main collapsed", True
        else:
            return "sidebar", "main", False

    # ----------------------------
    # ADMIN COLLAPSE
    # ----------------------------
    @app.callback(
        Output("admin-collapse", "is_open"),
        Input("admin-toggle", "n_clicks"),
        State("admin-collapse", "is_open"),
    )
    def toggle_admin(n, is_open):

        if n:
            return not is_open

        return is_open




    # ----------------------------
    # CARGAR AUTH
    # ----------------------------
    @app.callback(
        Output("auth-status", "data"),
        Input("url", "pathname"),
    )
    def cargar_auth(pathname):

        if 'user' in session:
            return {"usuario": session["user"], "es_admin": session["admin"]}

        return {"usuario": None, "es_admin": False}


    # ----------------------------
    # MOSTRAR ADMIN
    # ----------------------------
    @app.callback(
        Output("admin-toggle", "style"),
        Input("auth-status", "data"),
        prevent_initial_call=False
    )
    def mostrar_admin(data):

        if data and data.get("es_admin"):
            return {}

        return {"display": "none"}


    # ----------------------------
    # GESTIONAR USUARIOS
    # ----------------------------
    @app.callback(
        Output("usuarios-dropdown", "options"),
        Output("modal-confirmacion", "is_open"),
        Output("modal-confirmacion-anadir", "is_open"),
        Output("mensaje-usuario-eliminar", "children"),
        Output("mensaje-usuario-eliminar", "style"),
        Output("mensaje-usuario-anadir", "children"),
        Output("mensaje-usuario-anadir", "style"),
        Input("borrar-usuario-button", "n_clicks"),
        Input("cancelar-eliminar", "n_clicks"),
        Input("confirmar-eliminar", "n_clicks"),
        Input("add-usuario-button", "n_clicks"),
        Input("cancelar-anadir", "n_clicks"),
        Input("confirmar-anadir", "n_clicks"),
        State("modal-confirmacion", "is_open"),
        State("modal-confirmacion-anadir", "is_open"),
        State("usuarios-dropdown", "value"),
        State("input-usuario", "value"),
        State("input-passwd", "value"),
        State("check-admin", "value"),
    )
    def gestionar_usuarios(
        n_borrar, n_cancelar_del, n_confirmar_del,
        n_add, n_cancelar_add, n_confirmar_add,
        is_open_del, is_open_add,
        usuario_a_borrar, nuevo_usuario, nuevo_pass, es_admin
    ):

        ctx = dash.callback_context

        if not ctx.triggered:
            return dash.no_update, is_open_del, is_open_add, "", {"marginTop": "10px"}, "", {"marginTop": "10px"}

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        mensaje = ""
        estilo = {"marginTop": "10px"}
        opciones = dash.no_update

        try:

            if trigger_id == "borrar-usuario-button":
                return dash.no_update, True, is_open_add, "", estilo, "", estilo

            elif trigger_id == "cancelar-eliminar":
                return dash.no_update, False, is_open_add, "", estilo, "", estilo

            elif trigger_id == "confirmar-eliminar":

                qr.eliminar_usuario(usuario_a_borrar)

                usuarios_actualizados = pd.DataFrame(
                    qr.obtener_usuarios(),
                    columns=["id", "usuario"]
                )

                opciones = [
                    {'label': usu, 'value': usu}
                    for usu in usuarios_actualizados["usuario"].unique()
                ]

                mensaje = "✅ Usuario eliminado correctamente"
                estilo = {"color": "green", "marginTop": "10px"}

                return opciones, False, is_open_add, mensaje, estilo, "", estilo

            elif trigger_id == "add-usuario-button":
                return dash.no_update, is_open_del, True, "", estilo, "", estilo

            elif trigger_id == "cancelar-anadir":
                return dash.no_update, is_open_del, False, "", estilo, "", estilo

            elif trigger_id == "confirmar-anadir":

                qr.guardar_nuevo_usuario(nuevo_usuario, nuevo_pass, es_admin)

                usuarios_actualizados = pd.DataFrame(
                    qr.obtener_usuarios(),
                    columns=["id", "usuario"]
                )

                opciones = [
                    {'label': usu, 'value': usu}
                    for usu in usuarios_actualizados["usuario"].unique()
                ]

                mensaje = "✅ Usuario añadido correctamente"
                estilo = {"color": "green", "marginTop": "10px"}

                return opciones, is_open_del, False, "", estilo, mensaje, estilo

        except Exception as e:

            mensaje = f"❌ Error: {e}"
            estilo = {"color": "red", "marginTop": "10px"}

            return dash.no_update, is_open_del, is_open_add, mensaje, estilo, "", estilo

        return dash.no_update, is_open_del, is_open_add, "", estilo, "", estilo


    # ----------------------------
    # ELIMINAR AUDITORIA
    # ----------------------------
    @app.callback(
        Output("auditorias-dropdown", "options"),
        Output("mensaje-auditoria", "children"),
        Output("mensaje-auditoria", "style"),
        Input("borrar-auditoria-button", "n_clicks"),
        State("auditorias-dropdown", "value"),
        prevent_initial_call=True
    )
    def eliminar_auditoria_callback(n_clicks, auditoria_seleccionada):

        if not auditoria_seleccionada:

            return dash.no_update, "❌ Selecciona una auditoría para eliminar", {"color": "red"}

        try:

            qr.eliminar_auditoria(auditoria_seleccionada)

            df_actualizado = pd.DataFrame(
                qr.obtener_auditorias(),
                columns=["id", "nombre"]
            )

            opciones_actualizadas = [
                {"label": str(aud), "value": str(aud)}
                for aud in df_actualizado["nombre"].unique()
            ]

            return opciones_actualizadas, "✅ Auditoría eliminada correctamente", {"color": "green"}

        except Exception as e:

            return dash.no_update, f"❌ Error al eliminar la auditoría: {e}", {"color": "red"}
        


    @app.callback(
        Output("usuarios-dropdown", "options", allow_duplicate=True),
        Input("store-data", "data"),
        prevent_initial_call='initial_duplicate'
    )
    def cargar_usuarios(data):

        if not data:
            return []

        usuarios = qr.obtener_usuarios()

        df = pd.DataFrame(usuarios)

        return [
            {"label": row["usuario"], "value": row["id"]}
            for _, row in df.iterrows()
        ]
    
    @app.callback(
        Output("titulo-gestion", "children"),
        Output("label-auditorias", "children"),
        Output("borrar-auditoria-button", "children"),
        Input("store-idioma", "data")
    )
    def textos_gestion(idioma):

        return (
            qr.obtener_textos_interfaz(idioma, "gestion", "titulo"),
            qr.obtener_textos_interfaz(idioma, "gestion", "auditorias"),
            qr.obtener_textos_interfaz(idioma, "gestion", "titulo")
        )
    

    @app.callback(
        Output("titulo-usuarios-eliminar", "children"),
        Output("borrar-usuario-button", "children"),
        Output("cancelar-eliminar", "children"),
        Output("confirmar-eliminar", "children"),
        Output("usuarios-dropdown", "placeholder"),
        Output("modal-texto-eliminar", "children"),
        Output("modal-titulo-eliminar", "children"),
        Output("titulo-usuarios-anadir", "children"),
        Output("add-usuario-button", "children"),
        Output("modal-titulo-anadir", "children"),
        Output("modal-texto-anadir", "children"),
        Output("cancelar-anadir", "children"),
        Output("confirmar-anadir", "children"),
        Output("check-admin", "label"),
        Output("input-usuario", "placeholder"),
        Output("input-passwd", "placeholder"),
        Input("store-idioma", "data")
    )
    def textos_gestion(idioma):

        return (
            qr.obtener_textos_interfaz(idioma, "usuarios", "usuarios"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "eliminar_usuarios"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "cancelar"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "eliminar"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "seleccionar"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "msg_confirmacion"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "confirmacion"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "anadir_usuarios"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "anadir"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "confirmacion"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "msg_confirmacion_usu"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "cancelar"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "anadir"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "admin"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "usuario"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "passwd"),
        )
    
    @app.callback(
        Output("auditorias-dropdown", "options", allow_duplicate=True),
        Input("store-data", "data"),
        prevent_initial_call='initial_duplicate'
    )
    def cargar_auditorias(data):

        if not data:
            return []

        auditorias = qr.obtener_auditorias()

        df = pd.DataFrame(auditorias)

        return [
            {"label": row["nombre"], "value": row["id"]}
            for _, row in df.iterrows()
        ]