import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from app import app
from utils.constants import home_page_location, hyy_page_location, col_page_location
from pages.home import home
from pages.hyy import hyy
from pages.col import col_sonoro



@app.callback(
    Output("page-content", "children"), 
    [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == home_page_location:
        return home.layout
    #elif pathname == hyy_page_location:
    #    return hyy.layout
    elif pathname == col_page_location:
        return col_sonoro.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )