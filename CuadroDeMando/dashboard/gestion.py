from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def layout_gestion():
    return dcc.Loading(
        id="loading-gestion",
        type="circle",
        fullscreen=False,
        className='gestion-filtros',
        children=html.Div(
            className="gestion-container",
            children=[

                html.H2(
                    id="titulo-gestion",
                    className="gestion-titulo"
                ),

                html.Div(
                    className="gestion-fila",
                    children=[

                        html.Div(
                            className="gestion-campo",
                            children=[
                                dmc.Select(
                                    id="auditorias-dropdown",
                                    data=[],
                                    placeholder="Seleccione una auditoría",

                                    searchable=True,
                                    clearable=True,

                                    size="md",
                                    radius="md",
                                    variant="default",
                                    w=300,
                                ),
                            ],
                        ),

                        html.Div(
                            className="gestion-campo",
                            children=[
                                dmc.Select(
                                    id="versiones-dropdown",

                                    data=[],

                                    placeholder="Seleccione una versión",

                                    searchable=True,
                                    clearable=True,

                                    disabled=True,

                                    size="md",
                                    radius="md",
                                    variant="default",

                                    w=300,

                                    styles={
                                        "input": {
                                            "borderColor": "#dbe3ec",
                                            "backgroundColor": "white",
                                            "fontSize": "15px",
                                            "fontWeight": 500,
                                        }
                                    },
                                ),
                            ],
                        ),

                    ],
                ),

                dmc.Button(
                    id="borrar-auditoria-button",
                    n_clicks=0,
                    variant="outline",
                    color="red",
                    radius="md",
                    size="md",
                    w=250,
                    disabled=True,
                    leftSection=DashIconify(
                        icon="tabler:trash",
                        width=18
                    ),
                ),

                html.Div(
                    id="mensaje-auditoria",
                    className="gestion-mensaje"
                ),

            ],
        ),
    )