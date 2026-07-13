from dash import Output, Input, State, html, no_update
import dash
from dash.exceptions import PreventUpdate
from flask import session
import pandas as pd
import base64
import io
from dash import html

import data.querys as qr


def registrar_callbacks_upload(app):

    @app.callback(
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State('upload-data', 'last_modified')
    )
    def update_output(contents, filename, date):

        if contents is not None:

            return parse_contents(
                contents,
                filename,
                date
            )

        return None


    @app.callback(
        Output('file-upload-info', 'children'),
        Input('upload-data', 'filename'),
        Input('upload-data', 'contents'),
    )
    def update_upload_area(filename, content):

        if filename is not None and content is not None:

            return html.Div(
                [
                    html.Img(
                        src='https://img.icons8.com/color/48/microsoft-excel-2019--v1.png',
                        className="excel-icon"
                    ),

                    html.Span(
                        filename,
                        className="file-name"
                    )
                ],
                className="file-selected"
            )

        return ""

    @app.callback(
        Output("mensaje-importacion", "children"),
        Output("mensaje-importacion", "style"),
        Output("upload-data", "contents"),
        Output("input-texto", "value"),
        Output("dropdown-wcag", "value"),
        Output("dropdown-escala", "value"),
        Output("input-fecha", "value"),
        Input("btn-importar", "n_clicks"),
        State("upload-data", "contents"),
        State("input-texto", "value"),
        State("dropdown-wcag", "value"),
        State("dropdown-escala", "value"),
        State("input-fecha", "value"),
        State("store-idioma", "data"),
        prevent_initial_call=True
    )
    def importar_archivo(n_clicks, content, valor_dropdown, valor_wcag, valor_escala, fecha, idioma):

        try:

            if not content:
                return "Seleccione un archivo", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

            mensaje, estilo = procesar_y_guardar_archivo(
                content,
                valor_dropdown,
                valor_wcag,
                valor_escala,
                fecha,
                idioma
            )
            qr.registrar_auditoria(session.get('user'), "INSERT", "Auditoria insertada " + str(valor_dropdown))
            return mensaje, estilo, None, "", None, None, None

        except Exception as e:

            return f"Error durante la importación: {e}", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    
    @app.callback(
        Output("importar-titulo", "children"),
        Output("input-texto", "placeholder"),
        Output("input-fecha", "placeholder"),
        Output("dropdown-wcag", "placeholder"),
        Output("dropdown-escala", "placeholder"),
        Output("arrastra-ficheros", "children"),
        Output("btn-importar", "children"),
        Input("store-idioma", "data")
    )
    def textos_gestion(idioma):

        t = qr.obtener_textos_seccion(idioma, "auditorias")

        return (
            t["importar"],
            t["datos"],
            t["fecha"],
            t["versionwcag"],
            t["escala"],
            t["fichero"],
            t["guardar"],
)
    

    @app.callback(
        Output("dropdown-wcag", "data"),
        Input('url', 'pathname')
    )
    def dropdown_wcag(pathname):
        if pathname != "/dash/importar":
            raise PreventUpdate

        wcag = qr.obtener_tipos_wcag()

        opciones_wcag = [
            {"label": version, "value": str(id_)}
            for id_, version in wcag
        ]

        return opciones_wcag


    @app.callback(
        Output("dropdown-escala", "data"),
        Input('url', 'pathname')
    )
    def dropdown_escala(pathname):
        if pathname != "/dash/importar":
            raise PreventUpdate

        escalas = pd.DataFrame(qr.obtener_escalas())
        escala = pd.DataFrame(escalas.to_dict('records'))

        opciones_escala = [
            {"label": row["descripcion"], "value": str(row["id"])}
            for _, row in escala.iterrows()
        ]

        return opciones_escala
    

    @app.callback(
        Output("btn-importar", "disabled"),
        Input("input-texto", "value"),
        Input("input-fecha", "value"),
        Input("dropdown-wcag", "value"),
        Input("dropdown-escala", "value"),
        Input("upload-data", "contents"),
    )
    def activar_boton_cambiar_pwd(texto, fecha, wcag, escala, fichero):
        return not (fecha and wcag and escala and fichero and texto)
    


def procesar_y_guardar_archivo(
    content,
    valor_dropdown,
    valor_wcag,
    valor_escala,
    fecha,
    idioma
):

    try:

        textos = qr.obtener_textos_seccion(idioma, "importar")

        estilo = {
            "color": "red",
            "marginTop": "10px"
        }

        _, content_string = content.split(",")

        decoded = base64.b64decode(content_string)

        df = pd.read_excel(
            io.BytesIO(decoded),
            engine="openpyxl"
        )

        columnas_limpias = [
            col
            for col in df.columns
            if not col.startswith("Unnamed")
        ]

        with qr.engine.begin() as conn:

            tipo = qr.guardar_nuevo_tipo_entidad(
                conn,
                valor_dropdown,
                valor_escala,
                fecha,
                valor_wcag
            )

            if tipo == 0:
                return (
                    "❌ " + textos["tipo_entidad_ko"],
                    estilo
                )

            if qr.guardar_entidades(
                conn,
                tipo,
                columnas_limpias
            ) <= 0:
                return (
                    "❌ " + textos["entidad_ko"],
                    estilo
                )

            if qr.guardar_valores(
                conn,
                tipo,
                df
            ) <= 0:
                return (
                    "❌ " + textos["imp_auditoria_ko"],
                    estilo
                )

            estilo = {
                "color": "green",
                "marginTop": "10px"
            }

            return (
                "✅ " + textos["imp_auditoria_ok"],
                estilo
            )

    except Exception as error:

        print(error)


def parse_contents(contents, filename, date):

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    try:

        if filename.endswith('.xlsx'):

            df = pd.read_excel(
                io.BytesIO(decoded),
                engine="openpyxl"
            )

        elif filename.endswith('.xls'):

            df = pd.read_excel(
                io.BytesIO(decoded)
            )

        else:
            return html.Div(
                [
                    "Formato no soportado: ",
                    filename
                ]
            )


    except Exception as e:

        return html.Div(
            [
                "Error procesando el fichero: ",
                str(e)
            ]
        )


    return html.Div(
        [

            html.H5(filename),

            html.P(
                f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}"
            ),

            html.Hr(),

            html.Pre(
                df.head().to_string(),
                style={
                    "whiteSpace": "pre-wrap",
                    "maxHeight": "300px",
                    "overflowY": "auto"
                }
            )

        ]
    )