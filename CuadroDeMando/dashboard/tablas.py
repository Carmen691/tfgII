from dash import dash_table, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def layout_datos():

    return dcc.Loading(

        id="loading-datos",

        type="circle",

        fullscreen=False,

        children=html.Div(

            [

                html.H2(
                    id="titulo-datos",
                    className="gestion-titulo"
                ),

                html.Div(

                    dash_table.DataTable(

                    id="tabla-datos",
                    editable=True,

                    page_action="native",

                    page_current=0,

                    page_size=12,

                    sort_action="none",

                    data=[],

                    columns=[],
                    fixed_rows={
                        "headers": True
                    },

                    style_header={
                        "backgroundColor": "#f8fbff",
                        "color": "#1d4ed8",
                        "fontWeight": "600",
                        "fontSize": "15px",
                        "padding": "16px",
                        "border": "none",
                        "borderBottom": "2px solid #bfdbfe",
                    },

                    style_cell={
                        "fontFamily": "Inter, sans-serif",
                        "fontSize": "14px",
                        "border": "none",
                        "borderBottom": "1px solid #e5e7eb",
                        "backgroundColor": "white",
                        "color": "#334155",
                        "textAlign": "left",
                        "whiteSpace": "normal",
                        "padding": "10px 16px",
                        "height": "64px",
                        "minHeight": "64px",
                        "verticalAlign": "middle",

                    },

                    style_data_conditional=[
                        {
                            "if": {"state": "active"},
                            "backgroundColor": "#eff6ff",
                            "border": "1px solid #93c5fd",
                             "height": "72px",
                        },

                        {
                            "if": {"state": "selected"},
                            "backgroundColor": "#dbeafe",
                             "height": "72px",
                        },

                        # Hover
                        {
                            "if": {"state": "active"},
                            "backgroundColor": "#eff6ff",
                            "border": "1px solid #93c5fd",
                        },

                        # Conseguido
                        {
                            "if": {
                                "filter_query": '{Estado} = "Totalmente conseguido"'
                            },
                            "backgroundColor": "#c5f9e0",
                        },

                        # Parcialmente conseguido
                        {
                            "if": {
                                "filter_query": '{Estado} = "Ampliamente conseguido"'
                            },
                            "backgroundColor": "#d9fbeb",
                        },

                        # No conseguido
                        {
                            "if": {
                                "filter_query": '{Estado} = "No aplicable"'
                            },
                            "backgroundColor": "#fffbeb",
                        },

                        # No aplicable
                        {
                            "if": {
                                "filter_query": '{Estado} = "Parcialmente conseguido"'
                            },
                            "backgroundColor": "#f7dec5",
                        },

                        {
                            "if": {
                                "filter_query": '{Estado} = "No conseguido"'
                            },
                            "backgroundColor": "#f7c3c3",
                        },


                    ],

                    style_cell_conditional=[

                        {
                            "if": {"column_id": "Criterios"},
                            "width": "55%",
                        },

                        {
                            "if": {"column_id": "Entidades"},
                            "width": "15%",
                            "textAlign": "center",
                        },

                        {
                            "if": {"column_id": "Valores"},
                            "width": "30%",
                        },

                    ],

                ),

                    className="tabla-datos-container"

                ),

                html.Div(

                    [

                        dmc.Button(

                            id="btn-guardar-tabla",
                            disabled=True,
                            n_clicks=0,

                            variant="outline",

                            color="blue",

                            radius="md",

                            size="md",

                            w=250,

                            leftSection=DashIconify(
                                icon="tabler:device-floppy",
                                width=18
                            ),

                        ),

                        html.Div(

                            id="mensaje-guardar",

                            className="mensaje"

                        ),

                    ],

                    className="boton-con-mensaje"

                ),

            ],

            className="gestion-container"

        )

    )