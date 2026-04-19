from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import data.querys as bd



def layout_filtros(idioma, tiposEntidad, entidades, versionesWCAG, principios, niveles):   
    entidades = pd.DataFrame(entidades)
    versionesWCAG = pd.DataFrame(versionesWCAG)
    principios = pd.DataFrame(principios)
    niveles = pd.DataFrame(niveles)

    return html.Div([

        html.H5(bd.obtener_textos_interfaz(idioma, "filtros", "filtros"), style={"margin-bottom": "20px", "font-weight": "600"}),

        # Tipo entidad
        html.Label(bd.obtener_textos_interfaz(idioma, "filtros", "tipo_entidad"), style=label_style),
        dcc.Dropdown(
            id='tipo-entidad-dropdown',
            options = [
                {'label': e['nombre'], 'value': e['id']} for e in tiposEntidad],
            multi=False,
            persistence=True,
            persistence_type='session',
            style=input_style
        ),

        # Entidad
        html.Label(bd.obtener_textos_interfaz(idioma, "filtros", "entidades"), style=label_style),
        dcc.Dropdown(
            id='entidad-dropdown',
            options=[{'label': row['nombre'], 'value': row['id']} 
                     for _, row in entidades.drop_duplicates('id').iterrows()],
            multi=True,
            persistence=True,
            persistence_type='session',
            style=input_style
        ),

        # Principios
        html.Div(bd.obtener_textos_interfaz(idioma, "filtros", "principios"), style=section_title),
        dcc.Checklist(
            id='principios-checklist',
            options=[{'label': row['nombre'], 'value': row['id']} 
                     for _, row in principios.drop_duplicates('id').iterrows()],
            value=principios['id'].drop_duplicates().tolist(),
            labelStyle=checklist_style
        ),

        # 🔹 Versión
        html.Div(bd.obtener_textos_interfaz(idioma, "filtros", "version"), style=section_title),
        dcc.Checklist(
            id='wcag-version-checklist',
            options=[{'label': ver, 'value': ver} for ver in versionesWCAG["version"].unique()],
            value=versionesWCAG["version"].unique().tolist(),
            labelStyle=checklist_style
        ),

        # Nivel
        html.Div(bd.obtener_textos_interfaz(idioma, "filtros", "nivel"), style=section_title),
        dcc.Checklist(
            id='nivel-checklist',
            options=[{'label': niv, 'value': niv} for niv in niveles["nombre"].unique()],
            value=niveles['nombre'].drop_duplicates().tolist(),
            labelStyle=checklist_style
        ),

        html.Button(
            bd.obtener_textos_interfaz(idioma, "filtros", "actualizar"),
            id="boton-actualizar",
            n_clicks=0,
            className="btn-actualizar"
        )

], style={
    "padding": "10px 5px"
})

label_style = {
    "font-size": "13px",
    "font-weight": "500",
    "color": "#374151",
    "margin-top": "10px",
    "margin-bottom": "5px"
}

section_title = {
    "margin-top": "20px",
    "margin-bottom": "10px",
    "font-size": "14px",
    "font-weight": "600",
    "color": "#111827"
}

input_style = {
    "margin-bottom": "10px"
}

checklist_style = {
    "display": "block",
    "margin-bottom": "5px",
    "font-size": "13px"
}

