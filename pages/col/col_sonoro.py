from dash import html, dcc, dash_table
from pages.col.col_data import col_dataframe
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from utils.functions import drawText, drawFigure, drawInfo
from dash_iconify import DashIconify

col_df = col_dataframe()

header = dbc.Container([
                    dbc.Row([
                        dbc.Col(
                            html.H1("Soundmap of Colombia"),
                            style={'textAlign':'right','padding' : '0px'}),
                        dbc.Col(drawInfo(), width=3),
                        ], className='g-0'),
                    ], fluid=True)
header_metrics = dbc.Row([
                            dbc.Col([
                                    html.H3("Colombia Metrics"),
                                    html.Hr(),
                            ],  style={'textAlign': 'center'}),
                        ],)
metrics = dbc.Row([
                dbc.Card(
                    dcc.Graph(id='hablantes-indicator',
                      #className="h-100"
                    ),
                    style={'height':'100%','border':'none'},
                    className="p-0",
                    )],)
table = dbc.Row([
                dbc.Col([
                    html.H3("List of Native Languages",style={'text':'center', }),
                    dash_table.DataTable(
                            id='col-table', 
                            #export_format="csv",
                            page_action='native',
                            page_size=10,
                            style_as_list_view=True,
                            fixed_rows={'headers': True},
                            style_table={'height': '400px', 'overflowY': 'auto'},
                            style_cell={
                                'fontFamily': 'Open Sans',
                                'textAlign': 'left',
                                'height': '60px',
                                'padding': '2px 22px',
                                'whiteSpace': 'inherit',
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                            },)
                    ], style={'height':'100%', 'textAlign':'center'}),
                ])
col_map = dbc.Row([
                dbc.Card(
                    dcc.Graph(id='col-map-graph',
                      className="h-100"
                    ),
                    style={'height':'100%', 'border':'none'},
                    className="p-0",
                    )], )
controls = dbc.Row([
    dbc.Col([
        dmc.Accordion([
            dmc.AccordionItem(
                [
                    dmc.AccordionControl(
                        "Filters",
                        icon=DashIconify(
                            icon="material-symbols:filter-alt",
                            color=dmc.theme.DEFAULT_COLORS["blue"][6],
                            width=20,
                        ),
                    ),
                    dmc.AccordionPanel(
                        dbc.Row([
                            dbc.Col([dmc.Switch(id='test-switch', label='Test', checked=True)],width=2, align='center'),
                            dbc.Col([
                                dmc.MultiSelect(
                                    label="Select Linguistic Family",
                                    id='family-multiselector',
                                    data=[family for family in col_df['familia_linguistica'].unique()],
                                    style={"width": 200, "marginBottom": 10},
                                    clearable=True,
                                    searchable=True,
                                    nothingFound="No options found",

                                )]),
                            dbc.Col([
                                dmc.MultiSelect(
                                    label="Select State",
                                    id='depto-multiselector',
                                    data=[{'value':depto, 'label':depto.capitalize()} for depto in col_df['departamento'].unique()],
                                    style={"width": 200, "marginBottom": 10},
                                    clearable=True,
                                    searchable=True,
                                    nothingFound="No options found",

                                )]),
                        ]),
                    )
            ], value="customization")
        ]),
    ]),
    dbc.Col([
            dmc.Menu([
                        dmc.MenuTarget(dmc.Button('Menu',variant="light")),
                        dmc.MenuDropdown([
                        dmc.MenuItem(
                                    'Download Data',
                                    href="https://www.github.com/LauraTrujilloT",
                                    target="_blank",
                                    )
                        ])
                    ])
            ], width=4, style={'align-items':'center',}, align='center')
    ],justify='center', align="center")

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