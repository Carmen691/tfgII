import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
   


def creardash(app, datos, df, idioma, entidades):
    # Obtener datos de la base de datos
    print(datos)
    print(df.dtypes)
    print(df.head())  # Ver primeras filas
    # Crear una figura con Plotly
    #fig = px.bar(df, x="Categoria", y="Valores", title="Ejemplo de Dashboard con Dash")

    fig = px.bar(df, x="Entidades", y="Valores", 
             title="Cumplimiento de WCAG por Entidad",
             labels={"value": "Numero de Criterios", "variable": "Estado"},
             color ="Criterios",
             barmode="stack",
             category_orders={"Entidades": df["Entidades"].unique().tolist()})  # Forzar el orden de las entidades
             

    # Layout del Dashboard
    layout = html.Div([
        html.H1("Dashboard con Combos"),

        # Dropdown para seleccionar idioma
        html.Label("Selecciona un idioma:", style={'fontSize': '18px', 'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='idioma-dropdown',
            options=[{'label': cat, 'value': cat} for cat in idioma["nombre"].unique()],
            placeholder="Selecciona un idioma",
            multi=False,
            value="Espa\u00f1ol",
            style={'width': '50%', 'fontSize': '16px', 'padding': '5px'}
        ),

        # Dropdown para seleccionar idioma
        html.Label("Selecciona una entidad:", style={'fontSize': '18px', 'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='entidad-dropdown',
            options=[{'label': cat, 'value': cat} for cat in entidades["nombre"].unique()],
            placeholder="Selecciona una entidad",
            multi=True,
            style={'width': '50%', 'fontSize': '16px', 'padding': '5px'}
        ),

        # Gráfico
        dcc.Graph(id="grafico", figure=fig),

        # Tabla con los datos
        html.Label("Datos en tabla", style={'textAlign': 'center'}),
        dash_table.DataTable(
        id='tabla-datos',
        columns=[{"name": col, "id": col} for col in df.columns],
        #data=df.to_dict('records'),
        data=df.iloc[:10].to_dict('records'),
        # Estilo de la tabla
        style_table={'height': '400px', 'overflowY': 'auto', 'overflowX': 'auto'},  # Scroll vertical y horizontal
        style_cell={'textAlign': 'center', 'minWidth': '150px', 'width': '150px', 'maxWidth': '200px'},  # Ajustar tamaño de celdas
        style_header={'fontWeight': 'bold', 'backgroundColor': 'lightgrey'},  # Estilo del encabezado
        
        # Paginación
        page_size=10,  # Número de filas por página
        page_action='custom',  # Activar paginación
        page_current=0,

        # Filtros y ordenación
        #sort_action="native",  # Permitir ordenar columnas
        #filter_action="native"  # Permitir filtrar datos
    ),

    html.Div(
        style={'height': '30'}
    )

    ])

    return layout 


