from datetime import date

from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc


def layout_importar():

    return html.Div(

            [

                html.H2(
                    id="importar-titulo",
                    className="gestion-titulo"
                ),

                dcc.Store(id="refresh-trigger"),

                # =====================================================
                # DATOS
                # =====================================================

                html.Div(

                    [

                        html.Div(

                            [
                                dmc.TextInput(
                                    id="input-texto",
                                    radius="md",
                                    size="md",
                                    w=300,
                                ),

                            ],

                            className="gestion-campo"

                        ),

                        html.Div(

                            [
                                dmc.DateInput(
                                    id="input-fecha",
                                    radius="md",
                                    size="md",
                                    w=300,
                                    valueFormat="YYYY-MM-DD",
                                    maxDate=date.today()
                                ),

                            ],

                            className="gestion-campo"

                        ),

                    ],

                    className="gestion-fila"

                ),

                html.Div(

                    [

                        html.Div(

                            [
                                dmc.Select(
                                    id="dropdown-wcag",
                                    data=[],
                                    radius="md",
                                    size="md",
                                    w=300,
                                    clearable=True,
                                ),

                            ],

                            className="gestion-campo"

                        ),

                        html.Div(

                            [
                                dmc.Select(
                                    id="dropdown-escala",
                                    data=[],
                                    radius="md",
                                    size="md",
                                    w=300,
                                    clearable=True,
                                ),

                            ],

                            className="gestion-campo"

                        ),

                    ],

                    className="gestion-fila"

                ),

                # =====================================================
                # SUBIDA DE FICHERO
                # =====================================================

                html.Div(

                    [

                        dcc.Upload(

                            id="upload-data",

                            children=html.Div(

                                [

                                    DashIconify(
                                        icon="tabler:cloud-upload",
                                        width=34,
                                        color="#2563eb"
                                    ),

                                    html.Div(
                                        id="arrastra-ficheros",
                                        className="upload-texto"
                                    ),

                                    html.Div(
                                        "Excel (.xlsx, .xls)",
                                        className="upload-subtexto"
                                    ),

                                ],

                                className="upload-contenido"

                            ),

                            className="upload-importar",

                            multiple=False,

                            accept=".xlsx,.xls",

                        ),

                        html.Div(
                            id="file-upload-info",
                            className="file-upload-info"
                        ),

                    ],

                    className="upload-fila"

                ),

                # =====================================================
                # BOTÓN
                # =====================================================

                html.Div(

                    [

                        dmc.Button(
                            id="btn-importar",
                            n_clicks=0,
                            variant="outline",
                            color="blue",
                            radius="md",
                            size="md",
                            w=250,
                            disabled=True,
                            leftSection=DashIconify(
                                icon="tabler:upload",
                                width=18
                            ),
                        ),

                        html.Div(
                            id="mensaje-importacion",
                            className="mensaje"
                        ),

                    ],

                    className="boton-con-mensaje"

                ),

            ],

            className="gestion-container"

        )