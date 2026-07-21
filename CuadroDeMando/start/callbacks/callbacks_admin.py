import re

import bcrypt
import dash
from dash import Output, Input, State, callback_context
from dash import html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
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
        Output("sidebar", "className"),
        Output("main-content", "className"),
        Output("menu-collapsed", "data"),
        Input("admin-toggle", "n_clicks"),
        State("admin-collapse", "is_open"),
        State("menu-collapsed", "data"),
        prevent_initial_call=True
    )
    def toggle_admin(n, is_open, collapsed):

        if not n:
            raise PreventUpdate

        # Si está plegado, primero desplegar el menú
        if collapsed:
            return (
                True,
                "sidebar",
                "main",
                False
            )

        return (
            not is_open,
            "sidebar",
            "main",
            False
        )


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
        Output("usuarios-dropdown", "data"),
        Output("modal-confirmacion", "opened"),
        Output("modal-confirmacion-anadir", "opened"),
        Output("mensaje-usuario-eliminar", "children"),
        Output("mensaje-usuario-eliminar", "style"),
        Output("mensaje-usuario-anadir", "children"),
        Output("mensaje-usuario-anadir", "style"),
        Output("input-usuario", "value"),
        Output("input-passwd", "value"),
        Output("check-admin", "checked"),
        Input("borrar-usuario-button", "n_clicks"),
        Input("cancelar-eliminar", "n_clicks"),
        Input("confirmar-eliminar", "n_clicks"),
        Input("add-usuario-button", "n_clicks"),
        Input("cancelar-anadir", "n_clicks"),
        Input("confirmar-anadir", "n_clicks"),
        State("modal-confirmacion", "opened"),
        State("modal-confirmacion-anadir", "opened"),
        State("usuarios-dropdown", "value"),
        State("input-usuario", "value"),
        State("input-passwd", "value"),
        State("check-admin", "checked"),
        State("store-idioma", "data"),
    )
    def gestionar_usuarios(
        n_borrar,
        n_cancelar_del,
        n_confirmar_del,
        n_add,
        n_cancelar_add,
        n_confirmar_add,
        is_open_del,
        is_open_add,
        usuario_a_borrar,
        nuevo_usuario,
        nuevo_pass,
        es_admin,
        idioma,
    ):

        textos = qr.obtener_textos_seccion(idioma, "usuarios")

        ctx = dash.callback_context

        if not ctx.triggered:
            return (
                dash.no_update,
                is_open_del,
                is_open_add,
                "",
                {"marginTop": "10px"},
                "",
                {"marginTop": "10px"},
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        mensaje = ""
        estilo = {"marginTop": "10px"}
        opciones = dash.no_update

        def obtener_opciones_usuarios():
            df = pd.DataFrame(
                qr.obtener_usuarios_sin_actual(),
                columns=["id", "usuario"]
            )

            return [
                {
                    "label": row["usuario"],
                    "value": str(row["id"])
                }
                for _, row in df.iterrows()
            ]

        try:

            if trigger_id == "borrar-usuario-button":
                return (
                    dash.no_update,
                    True,
                    is_open_add,
                    "",
                    estilo,
                    "",
                    estilo,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                )

            elif trigger_id == "cancelar-eliminar":
                return (
                    dash.no_update,
                    False,
                    is_open_add,
                    "",
                    estilo,
                    "",
                    estilo,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                )

            elif trigger_id == "confirmar-eliminar":

                qr.eliminar_usuario(usuario_a_borrar)

                opciones = obtener_opciones_usuarios()

                qr.registrar_auditoria(
                    session.get("user"),
                    "DELETE",
                    "Usuario " + str(usuario_a_borrar) + " eliminado"
                )

                mensaje = "✅ " + textos["usuario_eliminado_ok"]
                estilo = {"color": "green", "marginTop": "10px"}

                return (
                    opciones,
                    False,
                    is_open_add,
                    mensaje,
                    estilo,
                    "",
                    estilo,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                )

            elif trigger_id == "add-usuario-button":
                return (
                    dash.no_update,
                    is_open_del,
                    True,
                    "",
                    estilo,
                    "",
                    estilo,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                )

            elif trigger_id == "cancelar-anadir":
                return (
                    dash.no_update,
                    is_open_del,
                    False,
                    "",
                    estilo,
                    "",
                    estilo,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                )

            elif trigger_id == "confirmar-anadir":

                estilo = {"color": "orange", "marginTop": "10px"}

                if len(nuevo_pass) < 7:
                    return (
                        dash.no_update,
                        is_open_del,
                        False,
                        "",
                        estilo,
                        textos["pwd_min_caract"],
                        estilo,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                    )

                if not re.search(r"[a-z]", nuevo_pass):
                    return (
                        dash.no_update,
                        is_open_del,
                        False,
                        "",
                        estilo,
                        textos["pwd_minuscula"],
                        estilo,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                    )

                if not re.search(r"[A-Z]", nuevo_pass):
                    return (
                        dash.no_update,
                        is_open_del,
                        False,
                        "",
                        estilo,
                        textos["pwd_mayuscula"],
                        estilo,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                    )

                if not re.search(r"\d", nuevo_pass):
                    return (
                        dash.no_update,
                        is_open_del,
                        False,
                        "",
                        estilo,
                        textos["pwd_numero"],
                        estilo,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                    )

                resultado = qr.guardar_nuevo_usuario(
                    nuevo_usuario,
                    nuevo_pass,
                    es_admin
                )

                if resultado == 0:

                    qr.registrar_auditoria(
                        session.get("user"),
                        "DELETE",
                        "Usuario " + str(nuevo_usuario) + " no añadido"
                    )

                    mensaje = "❌ " + textos["usuario_add_error"]
                    estilo = {"color": "red", "marginTop": "10px"}

                    return (
                        dash.no_update,
                        is_open_del,
                        False,
                        "",
                        estilo,
                        mensaje,
                        estilo,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                    )

                opciones = obtener_opciones_usuarios()

                qr.registrar_auditoria(
                    session.get("user"),
                    "DELETE",
                    "Usuario " + str(nuevo_usuario) + " añadido"
                )

                mensaje = "✅ " + textos["usuario_add"]
                estilo = {"color": "green", "marginTop": "10px"}

                return (
                    opciones,
                    is_open_del,
                    False,
                    "",
                    estilo,
                    mensaje,
                    estilo,
                    "",
                    "",
                    False,
                )

        except Exception as e:

            mensaje = "❌ Error: " + str(e)
            estilo = {"color": "red", "marginTop": "10px"}

            return (
                dash.no_update,
                is_open_del,
                is_open_add,
                mensaje,
                estilo,
                "",
                estilo,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        return (
            dash.no_update,
            is_open_del,
            is_open_add,
            "",
            estilo,
            "",
            estilo,
            dash.no_update,
            dash.no_update,
            dash.no_update,
        )

    # ----------------------------
    # ELIMINAR AUDITORIA
    # ----------------------------
    @app.callback(
        Output("auditorias-dropdown", "data"),
        Output("modal-confirmacion-auditoria", "opened"),
        Output("mensaje-auditoria", "children"),
        Output("mensaje-auditoria", "style"),
        Input("borrar-auditoria-button", "n_clicks"),
        Input("cancelar-auditoria", "n_clicks"),
        Input("confirmar-auditoria", "n_clicks"),
        State("modal-confirmacion-auditoria", "opened"),
        State("auditorias-dropdown", "value"),
        State("versiones-dropdown", "value"),
        State("store-idioma", "data"),
        prevent_initial_call=True
    )
    def eliminar_auditoria_callback(
        n_borrar,
        n_cancelar,
        n_confirmar,
        modal_abierto,
        auditoria_seleccionada,
        version_seleccionada,
        idioma
    ):

        textos = qr.obtener_textos_seccion(idioma, "auditorias")

        ctx = callback_context

        if not ctx.triggered:
            raise PreventUpdate

        trigger = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger == "borrar-auditoria-button":
            return (
                dash.no_update,
                True,
                "",
                {}
            )

        if trigger == "cancelar-auditoria":
            return (
                dash.no_update,
                False,
                "",
                {}
            )

        if trigger == "confirmar-auditoria":

            if not auditoria_seleccionada or not version_seleccionada:
                return (
                    dash.no_update,
                    False,
                    textos["auditorias_eliminar"],
                    {"color": "orange"}
                )

            try:

                qr.eliminar_auditoria(
                    auditoria_seleccionada,
                    version_seleccionada
                )

                df = pd.DataFrame(
                    qr.obtener_auditorias(),
                    columns=[
                        "id",
                        "nombre",
                        "idversion",
                        "fecha"
                    ]
                )

                opciones = [
                    {
                        "label": row["nombre"],
                        "value": str(row["id"])
                    }
                    for _, row in df.drop_duplicates(subset=["id"]).iterrows()
                ]

                qr.registrar_auditoria(
                    session.get("user"),
                    "DELETE",
                    f"Auditoria {auditoria_seleccionada} eliminada"
                )

                return (
                    opciones,
                    False,
                    textos["auditoria_eliminar_ok"],
                    {"color": "green"}
                )

            except Exception as e:

                return (
                    dash.no_update,
                    False,
                    textos["auditoria_eliminar_ko"] + ": " + str(e),
                    {"color": "red"}
                )

        raise PreventUpdate

    @app.callback(
        Output("usuarios-dropdown", "data", allow_duplicate=True),
        Input("url", "pathname"),
        prevent_initial_call='initial_duplicate'
    )
    def cargar_usuarios(pathname):

        if pathname != "/dash/administracion/usuarios":
            raise PreventUpdate

        usuarios = qr.obtener_usuarios_sin_actual()

        df = pd.DataFrame(usuarios)

        return [
            {"label": row["usuario"], "value": str(row["id"])}
            for _, row in df.iterrows()
        ]
    
    @app.callback(
        Output("titulo-gestion", "children"),
        Output("versiones-dropdown", "placeholder"),
        Output("auditorias-dropdown", "placeholder"),
        Output("borrar-auditoria-button", "children"),
        Output("titulo-modal-auditoria", "children"),
        Output("texto-modal-auditoria", "children"),
        Output("cancelar-auditoria", "children"),
        Output("confirmar-auditoria", "children"),
        Input("store-idioma", "data")
    )
    def textos_gestion(idioma):

        t = qr.obtener_textos_seccion(idioma, "gestion")

        return (
            t["titulo"],
            t["auditorias"],
            t["versiones"],
            [html.Span(t["eliminar"])],
            t["confirmacion"],
            t["msg_confirmacion"],
            t["cancelar"],
            t["eliminar"],
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
    def textos_usuarios(idioma):

        t = qr.obtener_textos_seccion(idioma, "usuarios")

        return (
            t["eliminar_usuarios"],
            t["eliminar"],
            t["cancelar"],
            t["eliminar"],
            t["seleccionar"],
            t["msg_confirmacion"],
            t["confirmacion"],
            t["anadir_usuarios"],
            t["anadir"],
            t["confirmacion"],
            t["msg_confirmacion_usu"],
            t["cancelar"],
            t["anadir"],
            t["admin"],
            t["usuario"],
            t["passwd"],
            t["cambiar_pwd"],
            t["pwd_actual"],
            t["nueva_pwd"],
            t["confirmar_pwd"],
            t["btn_cambiar_pwd"],
            t["btn_confirmar_pwd"],
            t["btn_body_pwd"],
            t["btn_cancelar_pwd"],
            t["btn_aceptar_pwd"]
        )
        
    @app.callback(
        Output("auditorias-dropdown", "data", allow_duplicate=True),
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
            {"label": row["nombre"], "value": str(row["id_tipo"])}
            for _, row in df.drop_duplicates(subset=["id_tipo"]).iterrows()
        ]

        return opciones_auditorias
    
    @app.callback(
        Output("versiones-dropdown", "disabled"),
        Input("auditorias-dropdown", "value")
    )
    def activar_versiones(auditoria_seleccionada):
        if auditoria_seleccionada:
            return False
        return True
    
    @app.callback(
        Output("versiones-dropdown", "data", allow_duplicate=True),
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
                "value": str(row["id_version"])
            }
            for _, row in df.iterrows()
        ]

        return opciones_versiones
    

    @app.callback(
        Output("modal-confirmacion-password", "opened"),
        Input("cambiar-password-button", "n_clicks"),
        Input("cancelar-password", "n_clicks"),
        Input("confirmar-password", "n_clicks"),
        State("modal-confirmacion-password", "opened"),
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
        Output("mensaje-password", "children"),
        Output("mensaje-password", "style"),
        Output("input-password-actual", "value"),
        Output("input-password-nueva", "value"),
        Output("input-password-confirmar", "value"),
        Input("confirmar-password", "n_clicks"),
        State("input-password-actual", "value"),
        State("input-password-nueva", "value"),
        State("input-password-confirmar", "value"),
        State("store-idioma", "data"),
        prevent_initial_call=True
    )
    def cambiar_password(n, actual, nueva, confirmar, idioma):

        usuario = session.get("user")

        textos_usuario = qr.obtener_textos_seccion(idioma, "usuarios")
        textos_sesion = qr.obtener_textos_seccion(idioma, "sesion")

        if not usuario:
            return (
                textos_sesion["sesion_exp"],
                {"color": "orange"},
                actual,
                nueva,
                confirmar
            )

        if nueva != confirmar:
            return (
                textos_usuario["pwd_change"],
                {"color": "orange"},
                actual,
                nueva,
                confirmar
            )

        if len(nueva) < 7:
            return (
                textos_usuario["pwd_min_caract"],
                {"color": "orange"},
                actual,
                nueva,
                confirmar
            )

        if actual == nueva:
            return (
                textos_usuario["pwd_coinciden"],
                {"color": "orange"},
                actual,
                nueva,
                confirmar
            )

        if not re.search(r"[a-z]", nueva):
            return (
                textos_usuario["pwd_minuscula"],
                {"color": "orange"},
                actual,
                nueva,
                confirmar
            )

        if not re.search(r"[A-Z]", nueva):
            return (
                textos_usuario["pwd_mayuscula"],
                {"color": "orange"},
                actual,
                nueva,
                confirmar
            )

        if not re.search(r"\d", nueva):
            return (
                textos_usuario["pwd_numero"],
                {"color": "orange"},
                actual,
                nueva,
                confirmar
            )

        passwd_guardada = qr.obtener_pwd(usuario)

        if not bcrypt.checkpw(
            actual.encode(),
            passwd_guardada.encode()
        ):
            return (
                textos_usuario["pwd_incorrecta"],
                {"color": "red"},
                actual,
                nueva,
                confirmar
            )

        nueva_hash = bcrypt.hashpw(
            nueva.encode(),
            bcrypt.gensalt()
        ).decode()

        qr.actualizar_password(
            usuario,
            nueva_hash
        )

        qr.registrar_auditoria(
            usuario,
            "UPDATE",
            f"Usuario {usuario} actualizó su contraseña"
        )

        return (
            textos_usuario["pwd_actualizada"],
            {"color": "green"},
            "",
            "",
            ""
        )

    @app.callback(
        Output("borrar-auditoria-button", "disabled"),
        Input("versiones-dropdown", "value"),
        Input("auditorias-dropdown", "value"),
    )
    def activar_boton_eliminar_aud(fecha, nombre):
        return not (nombre and fecha)
    

    @app.callback(
        Output("borrar-usuario-button", "disabled"),
        Input("usuarios-dropdown", "value"),
    )
    def activar_boton_eliminar_usu(usuario):
        return not (usuario)
    

    @app.callback(
        Output("add-usuario-button", "disabled"),
        Input("input-usuario", "value"),
        Input("input-passwd", "value"),
    )
    def activar_boton_anadir_usu(usuario, pwd):
        return not (usuario and pwd)
    
    @app.callback(
        Output("cambiar-password-button", "disabled"),
        Input("input-password-actual", "value"),
        Input("input-password-nueva", "value"),
        Input("input-password-confirmar", "value"),
    )
    def activar_boton_cambiar_pwd(actual, nueva, confirmar):
        return not (actual and nueva and confirmar)