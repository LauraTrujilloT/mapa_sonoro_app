from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

def formatter_2_decimals(x):
    '''returns float with 2 decimals
    _param (float) x
    _returns x
    '''
    return "{:.2f}".format(x)

# Text field
def drawText():
    return html.Div([
                    dbc.Card(
                        dbc.CardBody([
                            html.Div([
                                html.H5("Text"),
                                ], style={'textAlign': 'center'}) 
                            ])
                        ),
                    ])
def drawFigure(id_='fig-default'):
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(id=id_) 
            ])
        ),  
    ])

def drawInfo(text='Some help text'):
    return html.Div([
        html.I(DashIconify(
                            icon="ph:info",
                            #color=dmc.theme.DEFAULT_COLORS["blue"][6],
                            width=20,
                        ), id="target"),
        dbc.Tooltip(text, target="target"),
    ],
    className="text-muted",
    style = {
            #'background-color':'red',
            'align-items': 'center',
            'padding-top' : '5px',
            'height' : 'auto'}
)