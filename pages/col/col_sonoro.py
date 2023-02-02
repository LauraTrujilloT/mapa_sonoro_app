from dash import html, dcc
import dash_bootstrap_components as dbc
from components.col_components import *
import dash_mantine_components as dmc


layout = html.Div([
    header,
    html.Hr(),
    controls,
    html.Br(),
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    col_map,
                    ],md=7, style={'height':'100%'}
                ),
                dbc.Col([
                        header_metrics,
                        metrics,
                        html.Br(),
                        table
                ], md=5)
            ], align='center'),
            html.Br(),
            stats_components
        ],),
    ], body=True),
    dmc.Footer(
        height=60,
        fixed=True,
        children=[dmc.Text("A nice footer"), dmc.Text('@lvtrujillot')],
        style={"backgroundColor": "#f8f9fa"},
    )
])