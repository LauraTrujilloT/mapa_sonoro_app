from dash import html
from dash import dcc
from pages.col.col_data import col_dataframe
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from utils.functions import drawText, drawFigure, drawInfo


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Native Languages of Colombia"),style={'textAlign':'right','padding' : '0px'}),
            dbc.Col(drawInfo(), width=3),
        ], className='g-0'),
    html.Hr(),
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    drawFigure(id_='sonoro-graph')
                ], md=7),
                dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                    html.H5("Colombia Metrics"),
                                    html.Hr(),
                            ],  style={'textAlign': 'center'}),
                        ]),
                        dbc.Row([
                            dbc.Col([
                               drawText(),
                            ], width=4),
                            dbc.Col([
                               drawText(),
                            ], width=4),
                            dbc.Col([
                               drawText(),
                            ], width=4),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                               drawFigure(id_='sonoro-table')
                            ]),
                        ])
                ], md=5)
            ])
        ])
    ], body=True)
    ], fluid=True),
])