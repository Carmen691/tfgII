from dash import html, dcc


def layout_importar():

    return dcc.Loading(
        id="loading-importar",
        type="circle",
        fullscreen=False,

        children=html.Div([

            html.H2(
                id="importar-titulo"
            ),


            html.Br(),


            html.Label(
                id="entidad-datos"
            ),


            dcc.Store(
                id='refresh-trigger'
            ),


            dcc.Input(
                id='input-texto',
                type='text',
                debounce=True,
                className="input-style"
            ),


            html.Br(),
            html.Br(),


            html.Label(
                id="fecha-audit"
            ),


            dcc.Input(
                id='input-fecha',
                type='date',
                className="input-style"
            ),


            html.Br(),
            html.Br(),


            html.Label(
                id="version-wcag"
            ),


            dcc.Dropdown(
                id='dropdown-wcag',
                className="input-style"
            ),


            html.Br(),


            html.Label(
                id="escala-wcag"
            ),


            dcc.Dropdown(
                id='dropdown-escala',
                className="input-style"
            ),


            html.Br(),


            dcc.Upload(

                id='upload-data',

                children=html.Div(
                    id="arrastra-ficheros"
                ),

                className="upload-importar",

                multiple=False,

                accept='.xlsx,.xls',

            ),



            html.Div(
                id='file-upload-info'
            ),



            html.Div(

                [

                    html.Button(
                        id="btn-importar",
                        n_clicks=0,
                        className="btn-success"
                    ),


                    html.Div(
                        id="mensaje-importacion",
                        className="mensaje"
                    )

                ],

                className="boton-con-mensaje"

            )


        ])
    )