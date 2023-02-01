from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from pages.home.home_callbacks import make_col_map_home

style = {
    "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
    "textAlign": "center",
}

layout = html.Div([
                dmc.Title("Leveranging Dashboards with Plotly Dash", order=1),
                html.Hr(),
                dmc.Spoiler(
                            showLabel="Show more",
                            hideLabel="Hide",
                            maxHeight=50,
                            children=[
                                dmc.Text(
                                    """This talk will introduce Data Analysts/Enthusiasts into Plotly Dash,
                                    and how to build awesome dashboards using Python without 
                                    free trial limits nor prior CSS/HTML knowledge.
                                    """),
                                dmc.Blockquote(
                                    """ 
                                    Dash  is the original low-code framework for rapidly building data apps in Python, R, Julia, and F# (experimental).
                                    Written on top of Plotly.js and React.js, Dash is ideal for building and deploying data apps with customized user interfaces. It's particularly suited for anyone who works with data.
                                    Through a couple of simple patterns, Dash abstracts away all of the technologies and protocols that are required to build a full-stack web app with interactive data visualization.
                                    Dash is simple enough that you can bind a user interface to your code in less than 10 minutes.
                                    """,
                                    cite='Plotly Dash Documentation',
                                )
                            ],
                        ),
                html.Br(),
                dmc.Divider(variant='dotted'),
                html.Br(),
                dmc.Grid(
                    children=[
                        dmc.Col(
                            html.Div(children=[
                                dmc.Card(
                                        children=[
                                            dmc.CardSection([
                                                dmc.Image(
                                                    src="assets/img_natives_colombia.jpg",
                                                    #src="https://source.unsplash.com/bUlmNJqNO1o/",
                                                    height=200,
                                                ),
                                                dcc.Graph(
                                                    figure=make_col_map_home(), 
                                                    style={'height':800}),
                                        ]),
                                            dmc.Group(
                                                [
                                                    dmc.Text("Soundmap of Colombia", weight=500),
                                                ],
                                                position="apart",
                                                mt="md",
                                                mb="xs",
                                            ),
                                            dmc.Text(
                                                """This is a project built to show the advantages of using Dash in Analytics.
                                                The Soundmap of Colombia web app can be used to get a basic diagnosis and analytical description of the native languages
                                                in the country, and their risk of extinction, according to the data collected by Gobierno Nacional de Colombia.
                                                """,
                                                size="sm",
                                                color="dimmed",
                                            ),
                                            dmc.Menu(
                                                [
                                                    dmc.MenuItem(
                                                        dmc.Button(
                                                            "Go to Dashboard", 
                                                            leftIcon=DashIconify(icon="radix-icons:external-link"),
                                                            fullWidth=True,
                                                            variant='light',
                                                            color='blue',
                                                        ), href="/col"),
                                                ],
                                                transition="rotate-right",
                                                transitionDuration=150,
                                            ),
                                        ],
                                        withBorder=True,
                                        shadow="sm",
                                        radius="md",
                                        style={"width": '100%', 'height':'50%'},
                                    )
                            ],), span=8),
                        dmc.Col(
                            html.Div(children=[
                                        html.A(
                                            dmc.Tooltip(
                                                dmc.Avatar(
                                                    src="https://avatars.githubusercontent.com/LauraTrujilloT",
                                                    size="lg",
                                                    radius="xl",
                                                ),
                                                label="Laura Trujillo T",
                                                position="bottom",
                                            ),
                                            href="https://www.linkedin.com/in/lvtrujillot/",
                                            target="_blank",
                                        ),
                                        dmc.Text("About me", weight=500),
                                        dmc.Text("Hi there!", weight=250, align='unset'),
                                        dmc.Text("""I'm Laura and I'm currently working as Data Analyst @ Factored. """, weight=250),
                                        html.Hr(),
                                        dmc.Text('About Factored', weight=500),
                                        dmc.Text(
                                            """Factored was conceived in Palo Alto, California by Andrew Ng and 
                                                a team of highly experienced AI researchers, educators, and engineers to help address 
                                                the significant shortage of qualified AI 
                                                and machine learning engineers globally. 
                                                We know that exceptional technical aptitude, intelligence, 
                                                communication skills and passion are equally distributed around the world, 
                                                and we are committed to testing, vetting and nurturing 
                                                the most talented engineers on behalf of our clients.""", 
                                                weight=250), 
                                        html.Hr(),
                                        dmc.Text('About the Data', weight=500),
                                        dmc.Text(
                                            """The dataset contains information on the native languages 
                                            of the indigenous people, palanqueros, creoles,
                                            and gypsies who inhabit our territory and keep their language alive,
                                            as a fundamental part of their own identity.
                                            """, 
                                            weight=250),
                                        html.Br(),
                                        dmc.List(
                                                [
                                                    dmc.ListItem(dmc.Text("Start Date: May 18, 2017", weight=250), ),
                                                    dmc.ListItem(dmc.Text("Last Update: July 15, 2022", weight=250)),
                                                    dmc.ListItem(dmc.Text("Update Frequency: Every 3 years", weight=250)),
                                                    dmc.ListItem(dmc.Text("Geographical Coverage: National (Colombia)", weight=250)),
                                                    dmc.ListItem(
                                                        dmc.Text(
                                                            [
                                                                "Dataset collected by ",
                                                                dmc.Anchor(
                                                                    "Ministerio de Cultura de Colombia", href="https://www.datos.gov.co/Cultura/Mapa-Sonoro-Lenguas-Nativas-de-Colombia/734h-gxtn", 
                                                                    underline=False,
                                                                    target='_blank',
                                                                ),
                                                            ], weight=250
                                                        )
                                                    ),
                                                ], style={'color':'gray'}
                                            ),
                                        html.Hr(),
                                        dmc.Text('Useful Resources', weight=500),
                                        dmc.Navbar(
                                                    p="md",
                                                    width={"base": 300},
                                                    height=500,
                                                    children=[
                                                        dmc.Anchor("The Book of Dash, A.Schroeder, C. Mayer, and A.M Ward ", href="https://nostarch.com/book-dash", target='_blank'),
                                                        dmc.Anchor("YT Charming Data", href="https://www.youtube.com/@CharmingData/playlists",target='_blank'),
                                                        dmc.Anchor("Clean Architecture for AI/ML Applications using Dash", href="https://towardsdatascience.com/clean-architecture-for-ai-ml-applications-using-dash-and-plotly-with-docker-42a3eeba6233", target='_blank'),
                                                        dmc.Anchor("Interactive Python Dashboards with Plotly and Dash", href="https://www.udemy.com/course/interactive-python-dashboards-with-plotly-and-dash/", target='_blank'),
                                                        dmc.Anchor("Dash Gallery", href='https://dash.gallery/Portal/', target='_blank')
                                                    ],
                                                )

                        ]), span=4),
                    ],
                    gutter="xl",)
        ])