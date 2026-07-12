from dash import html, dcc


def layout_graficos():

    return dcc.Loading(

        id="loading-graficos",

        type="circle",

        fullscreen=False,

        children=html.Div(

            [

                html.H2(
                    id="titulo-graficos",
                    className="graficos-titulo"
                ),

                html.Div(

                    [

                        html.Div(
                            id="nombre_medicion",
                            className="grafico-chip"
                        ),

                        html.Div(
                            id="version_medicion",
                            className="grafico-chip grafico-chip-info"
                        ),

                    ],

                    className="grafico-header"

                ),

                html.Div(

                    [

                        html.Div(
                            id="datos-wcag-div",
                            className="grafico-card"
                        ),

                        html.Div(
                            id="cumplimiento-div",
                            className="grafico-card"
                        ),

                        html.Div(
                            id="niveles-div",
                            className="grafico-card"
                        ),

                    ],

                    className="grafico-cards"

                ),

                html.Div(

                    dcc.Graph(
                        id="grafico-porcentaje",
                        config={"displayModeBar": False}
                    ),

                    className="grafico-panel"

                ),

                html.Div(

                    dcc.Graph(
                        id="grafico-principios",
                        config={"displayModeBar": False}
                    ),

                    className="grafico-panel"

                ),

                html.Div(

                    dcc.Graph(
                        id="grafico-niveles",
                        config={"displayModeBar": False}
                    ),

                    className="grafico-panel"

                ),

                html.Div(

                    dcc.Graph(
                        id="grafico-heat",
                        config={"displayModeBar": False}
                    ),

                    className="grafico-panel"

                ),

                html.Div(

                    dcc.Graph(
                        id="grafico-problematicos",
                        config={"displayModeBar": False}
                    ),

                    className="grafico-panel"

                ),

            ],

            className="gestion-container"

        )

    )