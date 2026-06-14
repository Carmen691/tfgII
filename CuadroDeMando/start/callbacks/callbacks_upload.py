import dash
from dash import Output, Input, State, html, dash_table, no_update
from flask import app, session
import pandas as pd
import base64
import io
import datetime
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
        Output('upload-data', 'children'),
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
            html.Div('Arrastra o selecciona un archivo Excel'),
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
        Input("btn-importar", "n_clicks"),
        State("upload-data", "contents"),
        State("upload-data", "filename"),
        State("dropdown-sugerencias", "value"),
        State("dropdown-wcag", "value"),
        prevent_initial_call=True
    )
    def importar_archivo(
        n_clicks,
        content,
        filename,
        valor_dropdown,
        valor_wcag
    ):

        try:

            if not content:
                return "Seleccione un archivo"

            procesar_y_guardar_archivo(
                content,
                filename,
                valor_dropdown,
                valor_wcag
            )
            qr.registrar_auditoria(session.get('user'), "INSERT", "Auditoria insertada")
            return "Importación realizada correctamente"

        except Exception as e:

            return f"Error durante la importación: {e}"

    
    @app.callback(
        Output("importar-titulo", "children"),
        Output("entidad-datos", "children"),
        Output("dropdown-sugerencias", "placeholder"),
        Output("input-texto", "placeholder"),
        Output("add-option-button", "children"),
        Output("version-wcag", "children"),
        Output("dropdown-wcag", "placeholder"),
        Output("arrastra-ficheros", "children"),
        Output("btn-importar", "children"),
        Input("store-idioma", "data")
    )
    def textos_gestion(idioma):

        return (
            qr.obtener_textos_interfaz(idioma, "auditorias", "importar"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "datos"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "seleccionar"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "escribir"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "anadir"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "seleccionar"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "versionwcag"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "fichero"),
            qr.obtener_textos_interfaz(idioma, "auditorias", "guardar")
        )
    

    @app.callback(
        Output("dropdown-wcag", "options"),
        Input("store-data", "data"),
    )
    def cargar_importar(data):

        if not data:
            return []

        wcag = pd.DataFrame(data["tiposWCAG"])

        opciones_wcag = [
            {"label": row["version"], "value": row["id"]}
            for _, row in wcag.iterrows()
        ]

        return opciones_wcag

    @app.callback(
            Output("dropdown-sugerencias", "options"),
            Input("refresh-trigger", "data"),
            Input('store-data', 'data')
        )
    def actualizar_dropdown(_, data):
        if not data or "tiposEntidad" not in data:
            return no_update

        entidades = data["tiposEntidad"]

        if len(entidades) == 1 and isinstance(entidades[0], list):
            entidades = entidades[0]

        opciones = []
        for entidad in entidades:
            opciones.append({
                "label": entidad["nombre"],
                "value": entidad["id"]
            })

        return opciones

def procesar_y_guardar_archivo(content, filename, valor_dropdown, valor_wcag):

    try:

        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)

        df = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')

        columnas_limpias = [
            col for col in df.columns if not col.startswith('Unnamed')
        ]

        qr.guardar_entidades(valor_dropdown, columnas_limpias)

        result = qr.guardar_valores(valor_dropdown, valor_wcag, df)


    except Exception as error:

        print(error)