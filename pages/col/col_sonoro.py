from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from components.col_components import *

layout = html.Div([
    header,
    html.Hr(),
    controls,
    html.Br(),
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    #dcc.Graph(id="col-map-graph"),
                    col_map,
                ],
                    md=7,
                    style={'height':'100%'}
                ),
                dbc.Col([
                        header_metrics,
                        metrics,
                        html.Br(),
                        table
                ], md=5)
            ], align='center'),
        ],),
    ], body=True)
])