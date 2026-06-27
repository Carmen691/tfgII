import re

import bcrypt
import dash
from dash import Output, Input, State, callback_context
from dash.exceptions import PreventUpdate
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


    @app.callback(
        Output("link-auditorias","style"),
        Input("auth-status","data"),
    )
    def mostrar_menu_admin(auth):

        # todavía no cargó la sesión
        if auth is None:
            return {}

        if auth.get("es_admin"):
            return {}

        return {"display": "none"}

    @app.callback(
        Output("admin-eliminar-wrapper","style"),
        Output("admin-anadir-wrapper","style"),
        Input("auth-status","data"),
    )
    def mostrar_zonas_usuarios(auth):

        # todavía no se ha cargado la sesión
        if auth is None:
            return {}, {}

        if auth.get("es_admin"):
            return {}, {}

        oculto = {"display": "none"}

        return oculto, oculto


    @app.callback(
        Output("auth-status", "data"),
        Output("app-initialized", "data"),
        Input("app-initialized", "data"),
        prevent_initial_call=False
    )
    def cargar_auth(init):

        if init:
            raise PreventUpdate

        return (
            {
                "usuario": session.get("user"),
                "es_admin": bool(session.get("admin", False))
            },
            True
        )

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
        State("store-idioma", "data")
    )
    def gestionar_usuarios(
        n_borrar, n_cancelar_del, n_confirmar_del,
        n_add, n_cancelar_add, n_confirmar_add,
        is_open_del, is_open_add,
        usuario_a_borrar, nuevo_usuario, nuevo_pass, es_admin, idioma
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

                qr.registrar_auditoria(session.get('user'), "DELETE", "Usuario " + str(usuario_a_borrar) + " eliminado")
                mensaje = "✅ " + qr.obtener_textos_interfaz(idioma, "usuarios", "usuario_eliminado_ok")
                estilo = {"color": "green", "marginTop": "10px"}

                return opciones, False, is_open_add, mensaje, estilo, "", estilo

            elif trigger_id == "add-usuario-button":
                return dash.no_update, is_open_del, True, "", estilo, "", estilo

            elif trigger_id == "cancelar-anadir":
                return dash.no_update, is_open_del, False, "", estilo, "", estilo

            elif trigger_id == "confirmar-anadir":
                estilo = {"color": "orange", "marginTop": "10px"}
                if len(nuevo_pass) < 7:
                    return  dash.no_update, is_open_del, False, "", estilo, qr.obtener_textos_interfaz(idioma, "usuarios", "pwd_min_caract"), estilo

                if not re.search(r"[a-z]", nuevo_pass):
                    return dash.no_update, is_open_del, False, "", estilo, qr.obtener_textos_interfaz(idioma, "usuarios", "pwd_minuscula"), estilo

                if not re.search(r"[A-Z]", nuevo_pass):
                    return dash.no_update, is_open_del, False, "", estilo, qr.obtener_textos_interfaz(idioma, "usuarios", "pwd_mayuscula"), estilo

                if not re.search(r"\d", nuevo_pass):
                    return dash.no_update, is_open_del, False, "", estilo, qr.obtener_textos_interfaz(idioma, "usuarios", "pwd_numero"), estilo

                resultado = qr.guardar_nuevo_usuario(nuevo_usuario, nuevo_pass, es_admin)

                if resultado == 0:
                    qr.registrar_auditoria(session.get('user'), "DELETE", "Usuario " + str(nuevo_usuario) + " no añadido")
                    mensaje = "❌ " + qr.obtener_textos_interfaz(idioma, "usuarios", "usuario_add_error")
                    estilo = {"color": "red", "marginTop": "10px"}
                    return dash.no_update, is_open_del, False, "", estilo, mensaje, estilo


                usuarios_actualizados = pd.DataFrame(
                    qr.obtener_usuarios(),
                    columns=["id", "usuario"]
                )

                opciones = [
                    {'label': usu, 'value': usu}
                    for usu in usuarios_actualizados["usuario"].unique()
                ]

                qr.registrar_auditoria(session.get('user'), "DELETE", "Usuario " + str(nuevo_usuario) + " añadido")
                mensaje = "✅ " + qr.obtener_textos_interfaz(idioma, "usuarios", "usuario_add")
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
        State("versiones-dropdown", "value"),
        State("store-idioma", "data"),
        prevent_initial_call=True
    )
    def eliminar_auditoria_callback(n_clicks, auditoria_seleccionada, version_seleccionada, idioma):

        if not auditoria_seleccionada or not version_seleccionada:

            return dash.no_update, "❌ " + qr.obtener_textos_interfaz(idioma, "auditorias", "auditorias_eliminar"), {"color": "red"}

        try:

            qr.eliminar_auditoria(auditoria_seleccionada, version_seleccionada)

            df_actualizado = pd.DataFrame(
                qr.obtener_auditorias(),
                columns=["id", "nombre", "idversion", "fecha"]
            )

            opciones_actualizadas = [
                {"label": str(aud), "value": str(aud)}
                for aud in df_actualizado["nombre"].unique()
            ]
            qr.registrar_auditoria(session.get('user'), "DELETE", "Auditoria " + str(auditoria_seleccionada) + " eliminada")
            return opciones_actualizadas, "✅ " + qr.obtener_textos_interfaz(idioma, "auditorias", "auditoria_eliminar_ok"), {"color": "green"}

        except Exception as e:

            return dash.no_update, "❌ " + qr.obtener_textos_interfaz(idioma, "auditorias", "auditoria_eliminar_ko") + f": {e}", {"color": "red"}
        


    @app.callback(
        Output("usuarios-dropdown", "options", allow_duplicate=True),
        Input("url", "pathname"),
        prevent_initial_call='initial_duplicate'
    )
    def cargar_usuarios(pathname):

        if pathname != "/dash/administracion/usuarios":
            raise PreventUpdate

        usuarios = qr.obtener_usuarios()

        df = pd.DataFrame(usuarios)

        return [
            {"label": row["usuario"], "value": row["id"]}
            for _, row in df.iterrows()
        ]
    
    @app.callback(
        Output("titulo-gestion", "children"),
        Output("label-auditorias", "children"),
        Output("label-versiones", "children"),
        Output("borrar-auditoria-button", "children"),
        Output("versiones-dropdown", "placeholder"),
        Output("auditorias-dropdown", "placeholder"),
        Input("store-idioma", "data")
    )
    def textos_gestion(idioma):

        return (
            qr.obtener_textos_interfaz(idioma, "gestion", "titulo"),
            qr.obtener_textos_interfaz(idioma, "gestion", "auditorias"),
            qr.obtener_textos_interfaz(idioma, "gestion", "versiones"),
            qr.obtener_textos_interfaz(idioma, "gestion", "titulo"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "seleccionar"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "seleccionar")
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
        Output("titulo-cambiar-password", "children"),
        Output("input-password-actual", "placeholder"),
        Output("input-password-nueva", "placeholder"),
        Output("input-password-confirmar", "placeholder"),
        Output("cambiar-password-button", "children"),
        Output("btn-confirmar-cambio", "children"),
        Output("body-confirmar-cambio", "children"),
        Output("cancelar-password", "children"),
        Output("confirmar-password", "children"),
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
            qr.obtener_textos_interfaz(idioma, "usuarios", "cambiar_pwd"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "pwd_actual"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "nueva_pwd"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "confirmar_pwd"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "btn_cambiar_pwd"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "btn_confirmar_pwd"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "btn_body_pwd"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "btn_cancelar_pwd"),
            qr.obtener_textos_interfaz(idioma, "usuarios", "btn_aceptar_pwd"),
        )
    
    @app.callback(
        Output("auditorias-dropdown", "options", allow_duplicate=True),
        Input("url", "pathname"),
        prevent_initial_call='initial_duplicate'
    )
    def cargar_auditorias(pathname):
        if pathname != "/dash/administracion/auditorias":
            raise PreventUpdate
        
        auditorias = qr.obtener_auditorias()

        df = pd.DataFrame(
            auditorias,
            columns=["id_tipo", "nombre", "id_version", "fecha"]
        )

        opciones_auditorias = [
            {"label": row["nombre"], "value": row["id_tipo"]}
            for _, row in df.drop_duplicates(subset=["id_tipo"]).iterrows()
        ]

        return opciones_auditorias
    

    
    @app.callback(
        Output("versiones-dropdown", "options", allow_duplicate=True),
        Input("auditorias-dropdown", "value"),
        prevent_initial_call='initial_duplicate'
    )
    def cargar_auditorias(auditoria):

        if not auditoria:
            return []

        auditorias = qr.obtener_versiones_auditoria(auditoria)

        df = pd.DataFrame(
            auditorias,
            columns=["id_version", "fecha"]
        )

        opciones_versiones = [
            {
                "label": row["fecha"].strftime("%d/%m/%Y"),
                "value": row["id_version"]
            }
            for _, row in df.iterrows()
        ]

        return opciones_versiones
    

    @app.callback(
        Output("modal-confirmacion-password", "is_open"),
        Input("cambiar-password-button", "n_clicks"),
        Input("cancelar-password", "n_clicks"),
        Input("confirmar-password", "n_clicks"),
        State("modal-confirmacion-password", "is_open"),
        prevent_initial_call=True
    )
    def toggle_modal_password(
        btn_abrir,
        btn_cancelar,
        btn_confirmar,
        is_open
    ):

        return not is_open

    @app.callback(
        Output("mensaje-password","children"),
        Output("mensaje-password", "style"),
        Output("input-password-actual","value"),
        Output("input-password-nueva","value"),
        Output("input-password-confirmar","value"),
        Input("confirmar-password","n_clicks"),
        State("input-password-actual","value"),
        State("input-password-nueva","value"),
        State("input-password-confirmar","value"),
        State("store-idioma", "data"),
        prevent_initial_call=True
    )
    def cambiar_password(n, actual, nueva, confirmar, idioma):

        usuario = session.get("user")
        estilo = {"color": "orange", "marginTop": "10px"}
        if not usuario:
            return qr.obtener_textos_interfaz(idioma, "sesion", "sesion_exp"), estilo, actual, nueva, confirmar

        if nueva != confirmar:
            return qr.obtener_textos_interfaz(idioma, "usuarios", "pwd_change"), estilo, actual, nueva, confirmar

        if len(nueva) < 7:
            return qr.obtener_textos_interfaz(idioma, "usuarios", "pwd_min_caract"), estilo, actual, nueva, confirmar

        if not re.search(r"[a-z]", nueva):
            return qr.obtener_textos_interfaz(idioma, "usuarios", "pwd_minuscula"), estilo, actual, nueva, confirmar

        if not re.search(r"[A-Z]", nueva):
            return qr.obtener_textos_interfaz(idioma, "usuarios", "pwd_mayuscula"), estilo, actual, nueva, confirmar

        if not re.search(r"\d", nueva):
            return qr.obtener_textos_interfaz(idioma, "usuarios", "pwd_numero"), estilo, actual, nueva, confirmar

        passwd_guardada = qr.obtener_pwd(usuario)

        if not bcrypt.checkpw(
            actual.encode(),
            passwd_guardada.encode()
        ):
            estilo = {"color": "red", "marginTop": "10px"}
            return qr.obtener_textos_interfaz(idioma, "usuarios", "pwd_incorrecta"), estilo, actual, nueva, confirmar

        nueva_hash = bcrypt.hashpw(
            nueva.encode(),
            bcrypt.gensalt()
        ).decode()

        qr.actualizar_password(
            usuario,
            nueva_hash
        )
        qr.registrar_auditoria(session.get('user'), "UPDATE", "Usuario " + str(usuario) + " actualizó su contraseña")
        estilo = {"color": "green", "marginTop": "10px"}
        return (
            qr.obtener_textos_interfaz(idioma, "usuarios", "pwd_actualizada"),
            estilo,
            "",
            "",
            ""
        )
        


    @app.callback(
        Output("input-password-actual", "type"),
        Output("input-password-nueva", "type"),
        Output("input-password-confirmar", "type"),
        Input("ver-password-actual", "n_clicks"),
        Input("ver-password-nueva", "n_clicks"),
        Input("ver-password-confirmar", "n_clicks"),
        prevent_initial_call=True
    )
    def ver_password(actual, nueva, confirmar):

        boton = callback_context.triggered[0]["prop_id"].split(".")[0]

        if boton == "ver-password-actual":
            return (
                "text" if actual % 2 else "password",
                "password",
                "password"
            )

        if boton == "ver-password-nueva":
            return (
                "password",
                "text" if nueva % 2 else "password",
                "password"
            )

        if boton == "ver-password-confirmar":
            return (
                "password",
                "password",
                "text" if confirmar % 2 else "password"
            )
        
    @app.callback(
        Output("input-passwd", "type"),
        Input("ver-password-alta", "n_clicks"),
    )
    def ver_password_alta(n):
        return "text" if n and n % 2 else "password"