from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc


def layout_filtros():

    return dcc.Loading(

        id="loading-filtros",

        type="circle",

        children=html.Div(

            [

                html.H2(
                    id="titulo-filtros",
                    className="gestion-titulo"
                ),

                # ======================================================
                # FILTROS SUPERIORES
                # ======================================================

                html.Div(

                    [

                        html.Div(

                            [

                                html.Label(
                                    id="tipo_entidad",
                                    className="gestion-label"
                                ),

                                dmc.Select(
                                    id="tipo-entidad-dropdown",
                                    data=[],
                                    clearable=False,
                                    searchable=False,
                                    radius="md",
                                    size="md",
                                    w=300,
                                    persistence=True,
                                    persistence_type="session",
                                ),

                            ],

                            className="gestion-campo"

                        ),

                        html.Div(

                            [

                                html.Label(
                                    id="fecha_wcag",
                                    className="gestion-label"
                                ),

                                dmc.Select(
                                    id="version-auditoria-dropdown",
                                    data=[],
                                    clearable=False,
                                    searchable=False,
                                    radius="md",
                                    size="md",
                                    w=300,
                                    persistence=True,
                                    persistence_type="session",
                                ),

                            ],

                            className="gestion-campo"

                        ),

                    ],

                    className="gestion-fila"

                ),

                # ======================================================
                # ENTIDADES
                # ======================================================

                html.Div(

                    [

                        html.Label(
                            id="entidades",
                            className="gestion-label"
                        ),

                        html.Div(
                            [

                                dmc.ActionIcon(
                                    id="btn-seleccionar-todas",
                                    variant="subtle",
                                    color="blue",
                                    size="lg",
                                    children=DashIconify(
                                        icon="tabler:checks",
                                        width=18,
                                    ),
                                ),

                                html.Span(
                                    "Seleccionar todas",
                                    id="txt-seleccionar-todas",
                                    className="accion-entidades"
                                ),

                                dmc.ActionIcon(
                                    id="btn-deseleccionar",
                                    variant="subtle",
                                    color="red",
                                    size="lg",
                                    children=DashIconify(
                                        icon="tabler:x",
                                        width=18,
                                    ),
                                    style={"marginLeft": "24px"},
                                ),

                                html.Span(
                                    "Deseleccionar",
                                    id="txt-deseleccionar",
                                    className="accion-entidades"
                                ),

                            ],

                            className="acciones-entidades"

                        ),
                        dmc.MultiSelect(
                            id="entidad-dropdown",
                            data=[],
                            searchable=True,
                            clearable=True,
                            radius="md",
                            size="md",
                            style={"width": "100%", "maxWidth": "800px"},
                            persistence=True,
                            persistence_type="session",
                            leftSection=DashIconify(
                                icon="tabler:search",
                                width=16,
                                color="#64748b",
                            ),
                        ),

                    ],

                    className="gestion-campo"

                ),

                # ======================================================
                # CHECKLISTS
                # ======================================================

                html.Div(

                    [

                        # ---------------- PRINCIPIOS ----------------

                        html.Div(

                            [

                                html.Label(
                                    id="principios_wcag",
                                    className="gestion-label"
                                ),

                                dmc.CheckboxGroup(
                                    id="principios-checklist",
                                    children=[],
                                ),

                            ],

                            className="gestion-campo"

                        ),

                        # ---------------- VERSIONES ----------------

                        html.Div(

                            [

                                html.Label(
                                    id="version_wcag",
                                    className="gestion-label"
                                ),

                                dmc.CheckboxGroup(
                                    id="wcag-version-checklist",
                                    children=[],
                                ),

                            ],

                            className="gestion-campo"

                        ),

                        # ---------------- NIVEL ----------------

                        html.Div(

                            [

                                html.Label(
                                    id="nivel",
                                    className="gestion-label"
                                ),

                                dmc.CheckboxGroup(
                                    id="nivel-checklist",
                                    children=[],
                                ),

                            ],

                            className="gestion-campo"

                        ),

                    ],

                    className="gestion-fila"

                ),

                # ======================================================
                # BOTÓN
                # ======================================================

                html.Div(

                    [

                        dmc.Button(
                            id="boton-actualizar",
                            n_clicks=0,
                            variant="outline",
                            color="blue",
                            radius="md",
                            size="md",
                            w=250,
                            leftSection=DashIconify(
                                icon="tabler:filter-check",
                                width=18
                            ),
                        ),

                    ],

                    className="boton-con-mensaje"

                ),

            ],

            className="gestion-container"

        )

    )