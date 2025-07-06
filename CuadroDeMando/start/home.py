import copy
import datetime
from dashboard.filtros import layout_filtros
from dashboard.tablas import layout_datos
from dashboard.graficos import layout_graficos
from dashboard.usuarios import layout_usuarios
from dashboard.gestion import layout_gestion
from dashboard.importar import layout_importar
import dash
from dash import Dash, ctx, dcc, html, dash_table
import plotly.express as px
import pandas as pd
import data.querys as qr
from dashboard.layout import crear_layout
import io
import base64
import dash_bootstrap_components as dbc

external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.10.5/font/bootstrap-icons.min.css"
]



def crear_dash_app(flask_app): 
    idioma = pd.DataFrame(qr.obtener_idioma(), columns=["id", "codigo", "nombre"])
    entidades = pd.DataFrame(qr.obtener_entidades(), columns=["id", "nombre", "id_tipo"])
    usuarios = pd.DataFrame(qr.obtener_usuarios(), columns=["id", "usuario"])
    datos = pd.DataFrame(qr.obtener_datos(), columns = ["id_principio", "principio", "id_entidad", "entidad",
                                                        "id_criterio", "criterio", "id_descripcion", "descripcion", 
                                                        "observaciones", "version"])
    tiposEntidad = pd.DataFrame(qr.obtener_tipos_entidad(), columns=["id","nombre"])
    tiposWCAG = pd.DataFrame(qr.obtener_tipos_wcag(), columns=["id","version"])
    
    porcentaje_cumplimiento = pd.DataFrame(qr.obtener_suma_cumplimiento(), columns = ["principio", "num_no_conseguido",
                                            "num_parcialmente_conseguido", "num_no_aplicable",
                                            "num_ampliamente_conseguido", "num_totalmente_conseguido"])
    mapa_calor = pd.DataFrame(qr.obtener_mapa_calor(), columns = ["codigo_criterio", "nombre_criterio",
                            "codigo_pauta", "nombre_pauta", "nombre_principio", "no_conseguido",
                            "parcialmente_conseguido", "no_aplicable", "ampliamente_conseguido",
                            "totalmente_conseguido"])
    
    opciones_cumplimiento = pd.DataFrame(qr.obtener_opciones_cumplimiento(), columns = ["id_escala", "descripcion"])

    dropdown_opciones = [
        {"label": row["descripcion"], "value": row["id_escala"]}
        for index, row in opciones_cumplimiento.iterrows()
    ]

    # Datos de ejemplo
    df_datos = pd.DataFrame({
        "Criterios": datos["criterio"],
        "Valores": datos["id_descripcion"],
        "Entidades": datos["entidad"],
    })

    df_datos["Valores"] = df_datos["Valores"].astype(str)
    df_datos["Entidades"] = df_datos["Entidades"].astype(str)

    fig = px.bar(df_datos, x="Entidades", y="Valores", 
             title="Cumplimiento de WCAG por Entidad",
             labels={"value": "Numero de Criterios", "variable": "Estado"},
             color ="Criterios",
             barmode="stack",
             category_orders={"Entidades": df_datos["Entidades"].unique().tolist()})  # Forzar el orden de las entidades
    
    df_porcentajes = pd.DataFrame({
        "Principio" : porcentaje_cumplimiento["principio"],
        "No Conseguido": porcentaje_cumplimiento["num_no_conseguido"],
        "Parcialmente Conseguido": porcentaje_cumplimiento["num_parcialmente_conseguido"],
        "No Aplicable" : porcentaje_cumplimiento["num_no_aplicable"],
        "Ampliamente Conseguido" : porcentaje_cumplimiento["num_ampliamente_conseguido"],
        "Totalmente Conseguido" : porcentaje_cumplimiento["num_totalmente_conseguido"]
    })

    df_melt = df_porcentajes.melt(
        id_vars=["Principio"], 
        var_name="Estado", 
        value_name="Valores"
    )

    # Ahora sí puedes hacer el pie chart
    figPorcentaje = px.pie(
        df_melt,
        names="Estado",
        values="Valores",
        title="Cumplimiento de Principios"
    )


    # Calcula el porcentaje de cumplimiento
    mapa_calor["cumplimiento_total"] = mapa_calor["ampliamente_conseguido"] + mapa_calor["totalmente_conseguido"]

    mapa_calor["mediciones_totales"] = (
        mapa_calor["no_conseguido"] +
        mapa_calor["parcialmente_conseguido"] +
        mapa_calor["no_aplicable"] +
        mapa_calor["ampliamente_conseguido"] +
        mapa_calor["totalmente_conseguido"]
    )

    mapa_calor["porcentaje_cumplimiento"] = (mapa_calor["cumplimiento_total"] / mapa_calor["mediciones_totales"]) * 100

    figMapaCalor = px.density_heatmap(
        mapa_calor,
        x="codigo_pauta",         
        y="nombre_principio",
        z="porcentaje_cumplimiento",
        color_continuous_scale="Viridis",
        title="Mapa de calor de cumplimiento"
    )


    external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css']
    app = Dash(__name__, server=flask_app, url_base_pathname='/dash/', suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])


    layout_dashboard = crear_layout()
    app.layout = layout_dashboard


    @app.callback(
        dash.Output('page-content', 'children'),
        dash.Input('url', 'pathname')
    )
    def mostrar_contenido(pathname):    
        print("PATHNAME:", pathname)
        if pathname == '/dash/cuadroMando':
            return layout_graficos(fig, figPorcentaje, figMapaCalor)
        elif pathname == '/dash/datos':
            return layout_datos(df_datos, dropdown_opciones)
        elif pathname == '/dash/filtros':
            return layout_filtros(idioma, entidades)
        elif pathname == '/dash/administracion/usuarios':
            return layout_usuarios(idioma, usuarios)
        elif pathname == '/dash/administracion/auditorias':
            return layout_gestion(idioma, usuarios)
        elif pathname == '/dash/importar':
            return layout_importar(idioma, tiposEntidad, tiposWCAG)
        else:
            return html.H2("Página no encontrada")
    
    @app.callback(
        dash.Output("sidebar", "style"),
        dash.Output("menu-content", "style"),
        dash.Output("main-content", "style"),  # <-- nuevo
        dash.Output("menu-collapsed", "data"),
        dash.Input("toggle-menu", "n_clicks"),
        dash.State("menu-collapsed", "data"),
    )
    def toggle_menu(n_clicks, is_collapsed):
        if n_clicks is None:
            raise dash.exceptions.PreventUpdate

        collapsed = not is_collapsed

        if collapsed:
            sidebar_style = {
                "position": "fixed", "top": "0", "left": "0",
                "width": "40px", "height": "100%",
                "backgroundColor": "#2c3e50", "paddingTop": "20px",
                "zIndex": "1000", "overflow": "hidden"
            }
            menu_content_style = {"display": "none"}
            content_style = {"marginLeft": "50px", "transition": "margin-left 0.3s ease", "padding": "20px"}
        else:
            sidebar_style = {
                "position": "fixed", "top": "0", "left": "0",
                "width": "250px", "height": "100%",
                "backgroundColor": "#2c3e50", "paddingTop": "20px",
                "zIndex": "1000", "overflow": "hidden"
            }
            menu_content_style = {"display": "block"}
            content_style = {"marginLeft": "260px", "transition": "margin-left 0.3s ease", "padding": "20px"}

        return sidebar_style, menu_content_style, content_style, collapsed

    @app.callback(
        dash. Output("toggle-menu", "children"),
        dash.Input("menu-collapsed", "data")
    )
    def update_arrow(collapsed):
        return "⮞" if collapsed else "⮜"

    @app.callback(
        dash.Output('dropdown-celda', 'children'),
        dash.Output('store-celda-seleccionada', 'data'),
        dash.Input('tabla-datos', 'active_cell'),
        dash.State('tabla-datos', 'data'),
        prevent_initial_call=True
    )
    def mostrar_dropdown(active_cell, data):
        print("Celda activa:", active_cell)
        if not active_cell or active_cell["column_id"] != "Valores":
            return dash.no_update, None

        fila = active_cell["row"]
        valor_actual = data[fila]["Valores"]

        dropdown = dcc.Dropdown(
            id='dropdown-editor',
            options=[{'label': op['label'], 'value': op['value']} for op in dropdown_opciones],
            value=valor_actual,
            clearable=False
        )
        return dropdown, active_cell
    
    @app.callback(
        dash.Output('store-datos', 'data'),
        dash.Output('store-refresh-trigger', 'data'),
        dash.Input('dropdown-editor', 'value'),
        dash.State('store-celda-seleccionada', 'data'),
        dash.State('store-datos', 'data'),
        dash.State('tabla-datos', 'page_current'),
        dash.State('tabla-datos', 'page_size'),
        prevent_initial_call=True
    )
    def actualizar_valor_nuevo(valor_nuevo, celda_seleccionada, datos_store, page_current, page_size):
        if not celda_seleccionada:
            raise dash.exceptions.PreventUpdate

        fila_relativa = celda_seleccionada["row"]
        fila_absoluta = page_current * page_size + fila_relativa

        nuevos_datos = copy.deepcopy(datos_store)
        print(valor_nuevo)
        nuevos_datos[fila_absoluta]["Valores"] = valor_nuevo
        return nuevos_datos, {"refrescar": True}

    @app.callback(
        dash.Output('tabla-datos', 'data'),
        dash.Output('tabla-datos', 'page_count'),
        dash.Input('tabla-datos', 'page_current'),
        dash.Input('tabla-datos', 'page_size'),
        dash.Input('store-datos', 'data'),
    )
    def actualizar_o_refrescar_tabla(page_current, page_size, store_datos):
        ctx = dash.callback_context

        if not store_datos:
            return [], 0

        # Detectar qué input disparó el callback
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Si es la primera carga o cambio en store, mantenemos la página actual
        if triggered_id == "store-datos":
            # ¡IMPORTANTE! evitar usar valores None
            if page_current is None:
                page_current = 0
            if page_size is None:
                page_size = 10

        # Calcular paginación
        inicio = page_current * page_size
        fin = inicio + page_size
        page_count = -(-len(store_datos) // page_size)  # Redondeo hacia arriba

        return store_datos[inicio:fin], page_count
    
    @app.callback(dash.Output('output-data-upload', 'children'),
                dash.Input('upload-data', 'contents'),
                dash.State('upload-data', 'filename'),
                dash.State('upload-data', 'last_modified'))
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is not None:
            children = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
            return children
    
    @app.callback(
        dash.Output('file-upload-info', 'children'),
        dash.Output('upload-data', 'children'),
        dash.Output('upload-data', 'style'),
        dash.Input('upload-data', 'filename'),
        dash.Input('upload-data', 'contents'),
        dash.Input('btn-importar', 'n_clicks'),
        dash.Input('btn-cancelar', 'n_clicks'),
        dash.State('dropdown-sugerencias', 'value'),
        dash.State('dropdown-wcag', 'value'),
        prevent_initial_call=True  # Esto es para evitar que se active el callback al inicio
    )
    def update_upload_area(filename, content, btn_importar, btn_cancelar, valor_dropdown, valor_wcag):
        if btn_importar > 0:
            result_message= procesar_y_guardar_archivo(content, filename,valor_dropdown, valor_wcag)
        # Si el botón "Guardar datos" fue presionado, resetear el área
        if btn_importar > 0 or btn_cancelar > 0:
            return "", html.Div('Arrastra o selecciona un archivo Excel'), {
                'width': '100%',
                'height': '60px',  # Tamaño reducido cuando no hay archivo
                'lineHeight': '60px',  # Centrado vertical
                'borderWidth': '2px',
                'borderStyle': 'dashed',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '10px',
                'cursor': 'pointer',
                'padding': '10px'
            }

        # Si hay un archivo cargado, mostrar el ícono de Excel y el nombre
        if filename is not None and content is not None:
            return html.Div([
                html.Img(
                    src='https://img.icons8.com/color/48/microsoft-excel-2019--v1.png',
                    style={'height': '40px', 'marginBottom': '10px'}
                ),
                html.Div(f"{filename}", style={'wordWrap': 'break-word'})
            ]), "", {
                'width': '100%',
                'height': 'auto',  # El tamaño se ajusta al contenido
                'lineHeight': '60px',
                'borderWidth': '0px',  # No queremos borde punteado
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '10px',
                'cursor': 'pointer',
                'padding': '10px'
            }

        # Si no hay archivo cargado, mostrar el mensaje inicial y el borde punteado
        return "", html.Div('Arrastra o selecciona un archivo Excel'), {
            'width': '100%',
            'height': '60px',  # Tamaño reducido
            'lineHeight': '60px',  # Centrado vertical
            'borderWidth': '2px',
            'borderStyle': 'dashed',
            'borderRadius': '10px',
            'textAlign': 'center',
            'margin': '10px',
            'cursor': 'pointer',
            'padding': '10px'
        }
    
    # @app.callback(
    #     dash.Output('mensaje-confirmacion', 'children'),
    #     dash.Input('add-option-button', 'n_clicks'),
    #     dash.State('input-texto', 'value'),
    #     prevent_initial_call=True
    # )
    # def guardar_texto(n_clicks, valor_input):
    #     if valor_input:
    #         return qr.guardar_nuevo_tipo_entidad(valor_input)
    #     else:
    #         return 'No escribiste nada'

    @app.callback(
        [dash.Output('mensaje-confirmacion', 'children'),
        dash.Output('refresh-trigger', 'data')],
        dash.Input('add-option-button', 'n_clicks'),
        dash.State('input-texto', 'value'),
        prevent_initial_call=True
    )
    def guardar_texto(n_clicks, valor_input):
        if not valor_input:
            return 'No escribiste nada', dash.no_update

        mensaje = qr.guardar_nuevo_tipo_entidad(valor_input)
        
        # Cambia el contenido de refresh-trigger para forzar que otros callbacks dependientes se actualicen
        return mensaje, {'refresh': True}

    @app.callback(
        dash.Output("admin-collapse", "is_open"),
        dash.Input("admin-toggle", "n_clicks"),
        dash.State("admin-collapse", "is_open"),
        prevent_initial_call=True
    )
    def toggle_collapse(n_clicks, is_open):
        print(f"Click: {n_clicks}, Abierto: {is_open}") 
        return not is_open
     
    @app.callback(
        dash.Output("modal-confirmacion", "is_open"),
        [dash.Input("borrar-usuario-button", "n_clicks"),
        dash.Input("cancelar-eliminar", "n_clicks"),
        dash.Input("confirmar-eliminar", "n_clicks")],
        [dash.State("modal-confirmacion", "is_open")]
    )
    def toggle_modal(n_borrar, n_cancelar, n_confirmar, is_open):
        ctx = dash.callback_context
        if not ctx.triggered:
            return is_open
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "borrar-usuario-button":
            return True
        elif trigger_id in ["cancelar-eliminar", "confirmar-eliminar"]:
            return False
        return is_open
    

    @app.callback(
        dash.Output("usuarios-dropdown", "options"),
        dash.Input("confirmar-eliminacion", "n_clicks"),
        dash.State("usuarios-dropdown", "value"),
        prevent_initial_call=True
    )
    def eliminar_usuario(n_clicks, usuario_seleccionado):
        if usuario_seleccionado:
            # aquí va tu lógica para eliminar el usuario
            print(f"Eliminando usuario: {usuario_seleccionado}")
            # Recarga la lista de usuarios, actualiza el dropdown, etc.
        return [{'label': usu, 'value': usu} for usu in usuarios["usuario"].unique()]


    @app.callback(
        dash.Output("modal-confirmacion-anadir", "is_open"),
        [dash.Input("add-usuario-button", "n_clicks"),
        dash.Input("cancelar-anadir", "n_clicks"),
        dash.Input("confirmar-anadir", "n_clicks")],
        [dash.State("modal-confirmacion-anadir", "is_open")]
    )
    def toggle_modal_anadir(n_add, n_cancel, n_confirm, is_open):
        ctx = dash.callback_context
        if not ctx.triggered:
            return is_open
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "add-usuario-button":
            return True
        elif trigger_id in ["cancelar-anadir", "confirmar-anadir"]:
            return False
        return is_open
    
    @app.callback(
        dash.Output("mensaje-anadir", "children"),
        dash.Output("input-usuario", "value"),
        dash.Output("input-passwd", "value"),
        dash.Input("confirmar-anadir", "n_clicks"),
        dash.State("input-usuario", "value"),
        dash.State("input-passwd", "value"),
        dash.State("check-admin", "value"),
        prevent_initial_call=True
    )
    def confirmar_anadir_usuario(n_confirmar, usuario, passwd, admin):
        if n_confirmar:
            if not usuario or not passwd:
                return "⚠️ Por favor completa todos los campos.", dash.no_update, dash.no_update

            exito = qr.guardar_nuevo_usuario(usuario, passwd, bool(admin))
            if not exito:
                return "⚠️ El usuario ya existe. Usa otro nombre.", dash.no_update, dash.no_update

            return "✅ Usuario añadido correctamente.", "", ""
        
        # fallback si por algún motivo no entra en ninguno
        return dash.no_update, dash.no_update, dash.no_update
    
    @app.callback(
        dash.Output('borrar-usuario-button', 'disabled'),
        dash.Input('usuarios-dropdown', 'value')
    )
    def toggle_boton_eliminar(value):
        # Si no hay usuario seleccionado, deshabilita el botón
        return value is None or value == ''


    @app.callback(
        dash.Output('add-usuario-button', 'disabled'),
        [dash.Input('input-usuario', 'value'),
        dash.Input('input-passwd', 'value')]
    )
    def toggle_boton_añadir(usuario, passwd):
        # Deshabilita el botón si usuario o contraseña están vacíos o None
        if usuario and passwd:
            return False  # habilitar botón
        return True  # deshabilitar botón

    @app.callback(
        #dash.Output('tabla-datos', 'data'),
        #dash.Output('tabla-datos', 'columns'),
        dash.Output('grafico-general', 'figure'),
        dash.Output('grafico-porcentaje', 'figure'),
        dash.Output('grafico-mapa-calor', 'figure'),
        [
            dash.Input('idioma-dropdown', 'value'),
            dash.Input('entidad-dropdown', 'value'),
            dash.Input('principios-checklist', 'value'),
            dash.Input('wcag-version-checklist', 'value'),
            dash.Input('nivel-checklist', 'value'),
            dash.Input('pautas-dropdown', 'value'),
            dash.Input('agrupacion-radio', 'value'),
            dash.Input('escala-radio', 'value'),
        ]
    )
    def actualizar_datos(idioma, entidades, principios, versiones, niveles, pautas, agrupacion, escala):
        # Aquí haces el filtrado y generas los outputs correspondientes
        print('Hola')
        # Ejemplo mínimo
        data = [{"col1": "valor1", "col2": "valor2"}]
        columns = [{"name": "col1", "id": "col1"}, {"name": "col2", "id": "col2"}]
        figura_general = {}  # tu plotly figure
        figura_porcentaje = {}
        figura_mapa_calor = {}

        return data, columns, figura_general, figura_porcentaje, figura_mapa_calor

    return app

    
def parse_contents(contents, filename, date):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

        return html.Div([
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),

            dash_table.DataTable(
                df.to_dict('records'),
                [{'name': i, 'id': i} for i in df.columns]
            ),

            html.Hr(),  # horizontal line

            # For debugging, display the raw contents provided by the web browser
            html.Div('Raw Content'),
            html.Pre(contents[0:200] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
            })
        ])


def procesar_y_guardar_archivo(content, filename, valor_dropdown, valor_wcag):
    try:
        # Leemos el archivo Excel con pandas
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        # Usamos io.BytesIO para tratar el archivo en memoria como si fuera un archivo normal
        df = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')

        # Tipos que vamos a añadir a la tabla de entidades
        columnas_limpias = [col for col in df.columns if not col.startswith('Unnamed')]

        qr.guardar_entidades(valor_dropdown, columnas_limpias)

        qr.guardar_valores(valor_dropdown, valor_wcag, df)


        
        # Vamos a insertar 

        return
    except Exception as error:
        return ''
