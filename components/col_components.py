'''
'''
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from utils.functions import drawText, drawFigure, drawInfo
from dash import html, dcc, dash_table
from dash_iconify import DashIconify
from pages.col.col_data import col_dataframe

## Colombia SoundMap Dataframe
col_df = col_dataframe()
min_hablantes = int(col_df.n_hablantes.min())
half_hablantes=int(col_df.n_hablantes.max()/2)
max_hablantes = int(col_df.n_hablantes.max())

## Colors
map_colors = ['rgb(19, 32, 56)', 'rgb(50, 68, 83)', 'rgb(81, 102, 110)', 'rgb(112, 135, 137)', 'rgb(207, 216, 212)',
            'rgb(158, 160, 170)', '#8daad6', 'rgb(255,255,255)', '#4E5D6C',
            'rgb(231,231,231)','rgb(226,233,244)']

## Colombia SoundMap Layout Components

### Header and Dashboard Components
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
                    dmc.Text("Data Latest Update: July 15, 2022", color='gray',weight=500),
                    dmc.Text("* Data obtained from Datos Abiertos Colombia (datos.gov.co)", size='md'),
                    dmc.Text("** non-speaker locals are assumed to speak Spanish", size='md')
                ])
col_map = dbc.Row([
            dbc.Col([
                dbc.Card(
                    dcc.Graph(id='col-map-graph',
                      style={'height':'100%'}
                    ),
                    style={'border':'none'},
                    className="p-0",
                    ),
                dbc.Card(
                    dcc.Graph(id='bubble-legend',),# style={'height':100, 'width':500}), 
                    style={'width':'100%', 'border':'none'}, className='p-0'),
            ]),
        ],)

### Filters and Controls Components

#### Display Controls
display_controls = dbc.Col([
                            dmc.Accordion([
                                dmc.AccordionItem([
                                    dmc.AccordionControl(
                                        "Display Control"
                                    ),
                                dmc.AccordionPanel([
                                    dbc.Row([
                                        dbc.Col([
                                            dmc.Switch(
                                                id='carto-switch',
                                                label='Show Stats',
                                                checked=False,
                                            ),
                                            dmc.Switch(
                                                id='z-switch',
                                                label='Z Normalization',
                                                checked=True
                                            )
                                        ]),
                                        dbc.Col([
                                            dmc.Text("Colormap"),
                                            dmc.ColorPicker(
                                                id='colormap-picker',
                                                swatches=map_colors,
                                                swatchesPerRow=5,
                                                withPicker=False,
                                            ),
                                        ]),
                                    ])
                                ]),
                                ], value='customization')
                            ])
    ])

#### Full Control Panel
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
                    dmc.AccordionPanel([
                        dbc.Row([
                            dbc.Col([
                                dmc.MultiSelect(
                                    label="Select Specific Language",
                                    id='lengua-multiselector',
                                    data=[lengua for lengua in col_df['nombre_lengua'].sort_values(ascending=True).unique()],
                                    style={"width": 200, "marginBottom": 10},
                                    clearable=True,
                                    searchable=True,
                                    nothingFound="No options found",

                                ),
                            ]),
                            dbc.Col([
                                dmc.MultiSelect(
                                    label="Select Linguistic Family",
                                    id='family-multiselector',
                                    data=[family for family in col_df['familia_linguistica'].sort_values(ascending=True).unique()],
                                    style={"width": 200, "marginBottom": 10},
                                    clearable=True,
                                    searchable=True,
                                    nothingFound="No options found",

                                ),
                            ]),
                            dbc.Col([
                                dmc.MultiSelect(
                                    label="Select State",
                                    id='depto-multiselector',
                                    data=[{'value':depto, 'label':depto.capitalize()} for depto in col_df['departamento'].sort_values(ascending=True).unique()],
                                    style={"width": 200, "marginBottom": 10},
                                    clearable=True,
                                    searchable=True,
                                    nothingFound="No options found",

                                ),
                            ]),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dmc.Text('Select Max Total of Speakers'),
                                dmc.Slider(
                                    id='hablantes-slider',
                                    style={'marginBottom':10},
                                    max=col_df.n_hablantes.max(),
                                    min=col_df.n_hablantes.min(),
                                    value=col_df.n_hablantes.max(),
                                    marks=[
                                        {'value':col_df.n_hablantes.min(), 'label': f'{min_hablantes:,}'},
                                        {'value':col_df.n_hablantes.max()/2, 'label':f'{half_hablantes:,}'},
                                        {'value':col_df.n_hablantes.max(), 'label':f'{max_hablantes:,}'}
                                    ]
                                ),
                            ]),
                        ]),
                ])
            ], value="customization")
        ]),
    ], ),
    display_controls,
    dbc.Col([
            dmc.Menu([
                        dmc.MenuTarget(dmc.Button('Menu',variant="light")),
                        dmc.MenuDropdown([
                            dmc.MenuItem(
                                        'Github Repository',
                                        href="https://www.github.com/LauraTrujilloT",
                                        target="_blank",
                                        ),
                            dmc.MenuItem(
                                        'Download Data',
                                        href="https://www.github.com/LauraTrujilloT",
                                        target="_blank",
                                        ),
                            dmc.MenuItem(
                                    'Help',
                                    href="https://www.github.com/LauraTrujilloT",
                                    target="_blank",
                                    )
                        ])
                    ])
            ],md=2 , style={'align-items':'center',}, align='center')
    ],justify='center', align="center")