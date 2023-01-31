from dash import html
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

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
                                    Dash  is the original low-code framework for rapidly building data apps in Python, R, Julia, and F# (experimental).
                                    Written on top of Plotly.js and React.js, Dash is ideal for building and deploying data apps with customized user interfaces. It's particularly suited for anyone who works with data.
                                    Through a couple of simple patterns, Dash abstracts away all of the technologies and protocols that are required to build a full-stack web app with interactive data visualization.
                                    Dash is simple enough that you can bind a user interface to your code in less than 10 minutes."""
                                )
                            ],
                        ),
                html.Br(),
                dmc.Grid(
                    children=[
                        dmc.Col(
                            html.Div(children=[
                                dmc.Card(
                                        children=[
                                            dmc.CardSection(
                                                dmc.Image(
                                                    #src="assets/img_natives_colombia.jpg",
                                                    src="https://source.unsplash.com/bUlmNJqNO1o/",
                                                    #height=160,
                                                )
                                            ),
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
                                        dmc.Text("Something super interesting", weight=250), 
                                        html.Hr(),
                                        dmc.Text('About the Data', weight=500),
                                        dmc.Text("Something super interesting", weight=250),
                                        html.Hr(),
                                        dmc.Text('Useful Resources', weight=500),
                                        dmc.Navbar(
                                                    p="md",
                                                    width={"base": 300},
                                                    height=500,
                                                    children=[
                                                        dmc.Anchor("Link1", href="/"),
                                                        dmc.Anchor("Link2", href="/"),
                                                        dmc.Anchor("Link3", href="/"),
                                                        dmc.Anchor("Link4", href="/"),
                                                    ],
                                                )

                        ]), span=4),
                    ],
                    gutter="xl",)
        ])