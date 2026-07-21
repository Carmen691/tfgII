from dash import dash_table, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def layout_datos():

    return html.Div(

            [

                html.H2(
                    id="titulo-datos",
                    className="gestion-titulo"
                ),

                html.Div(

                    dash_table.DataTable(

                    id="tabla-datos",

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
                         "height": "auto",
                        "verticalAlign": "middle",

                    },

                    style_data_conditional=[

                    # -------------------------
                    # Sin borde al seleccionar
                    # -------------------------

                    {
                        "if": {"state": "active"},
                        "border": "none",
                    },

                    {
                        "if": {"state": "selected"},
                        "border": "none",
                    },

                    # =========================
                    # Totalmente conseguido
                    # =========================

                    {
                        "if": {
                            "filter_query": '{Estado} = "Totalmente conseguido"'
                        },
                        "backgroundColor": "#c5f9e0",
                    },
                    {
                        "if": {
                            "state": "active",
                            "filter_query": '{Estado} = "Totalmente conseguido"'
                        },
                        "backgroundColor": "#c5f9e0",
                        "border": "none",
                    },
                    {
                        "if": {
                            "state": "selected",
                            "filter_query": '{Estado} = "Totalmente conseguido"'
                        },
                        "backgroundColor": "#c5f9e0",
                        "border": "none",
                    },

                    # =========================
                    # Ampliamente conseguido
                    # =========================

                    {
                        "if": {
                            "filter_query": '{Estado} = "Ampliamente conseguido"'
                        },
                        "backgroundColor": "#d9fbeb",
                    },
                    {
                        "if": {
                            "state": "active",
                            "filter_query": '{Estado} = "Ampliamente conseguido"'
                        },
                        "backgroundColor": "#d9fbeb",
                        "border": "none",
                    },
                    {
                        "if": {
                            "state": "selected",
                            "filter_query": '{Estado} = "Ampliamente conseguido"'
                        },
                        "backgroundColor": "#d9fbeb",
                        "border": "none",
                    },

                    # =========================
                    # No aplicable
                    # =========================

                    {
                        "if": {
                            "filter_query": '{Estado} = "No aplicable"'
                        },
                        "backgroundColor": "#fffbeb",
                    },
                    {
                        "if": {
                            "state": "active",
                            "filter_query": '{Estado} = "No aplicable"'
                        },
                        "backgroundColor": "#fffbeb",
                        "border": "none",
                    },
                    {
                        "if": {
                            "state": "selected",
                            "filter_query": '{Estado} = "No aplicable"'
                        },
                        "backgroundColor": "#fffbeb",
                        "border": "none",
                    },

                    # =========================
                    # Parcialmente conseguido
                    # =========================

                    {
                        "if": {
                            "filter_query": '{Estado} = "Parcialmente conseguido"'
                        },
                        "backgroundColor": "#f7dec5",
                    },
                    {
                        "if": {
                            "state": "active",
                            "filter_query": '{Estado} = "Parcialmente conseguido"'
                        },
                        "backgroundColor": "#f7dec5",
                        "border": "none",
                    },
                    {
                        "if": {
                            "state": "selected",
                            "filter_query": '{Estado} = "Parcialmente conseguido"'
                        },
                        "backgroundColor": "#f7dec5",
                        "border": "none",
                    },

                    # =========================
                    # No conseguido
                    # =========================

                    {
                        "if": {
                            "filter_query": '{Estado} = "No conseguido"'
                        },
                        "backgroundColor": "#f7c3c3",
                    },
                    {
                        "if": {
                            "state": "active",
                            "filter_query": '{Estado} = "No conseguido"'
                        },
                        "backgroundColor": "#f7c3c3",
                        "border": "none",
                    },
                    {
                        "if": {
                            "state": "selected",
                            "filter_query": '{Estado} = "No conseguido"'
                        },
                        "backgroundColor": "#f7c3c3",
                        "border": "none",
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