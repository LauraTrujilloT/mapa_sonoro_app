from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

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
        html.I(className="fas fa-question-circle fa-lg", id="target"),
        dbc.Tooltip("Some help text", target="target"),
    ],
    className="text-muted",style = {
                    #'background-color':'red',
                    'align-items': 'center',
                    'padding-top' : '5px',
                    'height' : 'auto'}
)