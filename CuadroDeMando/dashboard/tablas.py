from dash import dash_table, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def layout_datos():

    return html.Div(

            [
                dcc.Interval(
                    id="tabla-ready",
                    interval=1,
                    n_intervals=0,
                    max_intervals=1
                ),
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

                    style_data_conditional=[],

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