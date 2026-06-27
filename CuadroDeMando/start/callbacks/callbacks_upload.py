import dash
from dash import Output, Input, State, html, dash_table, no_update
from dash.exceptions import PreventUpdate
from flask import app, session
import pandas as pd
import base64
import io
import datetime

from sqlalchemy import engine
import data.querys as qr


def registrar_callbacks_upload(app):

    @app.callback(
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State('upload-data', 'last_modified')
    )
    def update_output(list_of_contents, list_of_names, list_of_dates):

        if list_of_contents is not None:

            children = [
                parse_contents(c, n, d)
                for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
            ]

            return children


    @app.callback(
        Output('file-upload-info', 'children'),
        Output('upload-data', 'style'),
        Input('upload-data', 'filename'),
        Input('upload-data', 'contents'),
    )
    def update_upload_area(filename, content):

        if filename is not None and content is not None:

            return (
                html.Div([
                    html.Img(
                        src='https://img.icons8.com/color/48/microsoft-excel-2019--v1.png',
                        style={
                            'height': '40px',
                            'marginBottom': '10px'
                        }
                    ),
                    html.Div(
                        filename,
                        style={'wordWrap': 'break-word'}
                    )
                ]),
                "",
                {
                    'width': '100%',
                    'height': 'auto',
                    'lineHeight': '60px',
                    'borderWidth': '0px',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'cursor': 'pointer',
                    'padding': '10px'
                }
            )

        return (
            "",
            {
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '2px',
                'borderStyle': 'dashed',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '10px',
                'cursor': 'pointer',
                'padding': '10px'
            }
        )

    @app.callback(
        Output("mensaje-importacion", "children"),
        Output("mensaje-importacion", "style"),
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
                return "Seleccione un archivo"

            resultado = procesar_y_guardar_archivo(
                content,
                valor_dropdown,
                valor_wcag,
                valor_escala,
                fecha,
                idioma
            )
            qr.registrar_auditoria(session.get('user'), "INSERT", "Auditoria insertada " + str(valor_dropdown))
            return resultado

        except Exception as e:

            return f"Error durante la importación: {e}"

    
    @app.callback(
        Output("importar-titulo", "children"),
        Output("entidad-datos", "children"),
        Output("fecha-audit", "children"),
        Output("input-texto", "placeholder"),
        Output("dropdown-wcag", "placeholder"),
        Output("version-wcag", "children"),
        Output("escala-wcag", "children"),
        Output("dropdown-escala", "placeholder"),
        Output("arrastra-ficheros", "children"),
        Output("btn-importar", "children"),
        Input("store-idioma", "data")
    )
    def textos_gestion(idioma):

        return (
            qr.obtener_textos_interfaz(idioma, "auditorias", "importar"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "datos"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "fecha"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "escribir"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "seleccionar"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "versionwcag"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "escala"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "seleccionar"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "fichero"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "guardar")
        )
    

    @app.callback(
        Output("dropdown-wcag", "options"),
        Input('url', 'pathname'),   
        State("store-idioma", "data")
    )
    def dropdown_wcag(pathname):
        if pathname != "/dash/importar":
            raise PreventUpdate

        wcag = qr.obtener_tipos_wcag()

        opciones_wcag = [
            {"label": row["version"], "value": row["id"]}
            for _, row in wcag.iterrows()
        ]

        return opciones_wcag


    @app.callback(
        Output("dropdown-escala", "options"),
        Input('url', 'pathname')
    )
    def dropdown_escala(pathname):
        if pathname != "/dash/importar":
            raise PreventUpdate

        escalas = pd.DataFrame(qr.obtener_escalas())
        escala = pd.DataFrame(escalas.to_dict('records'))

        opciones_escala = [
            {"label": row["descripcion"], "value": row["id"]}
            for _, row in escala.iterrows()
        ]

        return opciones_escala

def procesar_y_guardar_archivo(content, valor_dropdown, valor_wcag, valor_escala, fecha, idioma):

    try:
        estilo = {"color": "red", "marginTop": "10px"}
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)

        df = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')

        columnas_limpias = [
            col for col in df.columns if not col.startswith('Unnamed')
        ]
        with qr.engine.begin() as conn:
            tipo = qr.guardar_nuevo_tipo_entidad(conn, valor_dropdown, valor_escala, fecha)

            if tipo == 0:
                return '❌ ' + qr.obtener_textos_interfaz(idioma, "importar", "tipo_entidad_ko"), estilo
            else:
                if qr.guardar_entidades(conn, tipo, columnas_limpias) > 0:
                    if qr.guardar_valores(conn, tipo, valor_wcag, df) > 0:
                        estilo = {"color": "green", "marginTop": "10px"}
                        return '✅' + qr.obtener_textos_interfaz(idioma, "importar", "imp_auditoria_ok"), estilo
                    else:
                        return '❌ ' + qr.obtener_textos_interfaz(idioma, "importar", "imp_auditoria_ko"), estilo
                else:
                    return '❌ ' + qr.obtener_textos_interfaz(idioma, "importar", "entidad_ko"), estilo

    except Exception as error:

        print(error)