import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from app import app
from utils.constants import home_page_location,  col_page_location
from pages.home import home
from pages.col import col_sonoro



@app.callback(
    Output("page-content", "children"), 
    [Input("url", "pathname")])
def render_page_content(pathname):
    print("Check URL Pathname : ", pathname)
    if pathname == home_page_location:
        return home.layout
    elif pathname == col_page_location:
        return col_sonoro.layout
    return html.Div(
        dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"Uh Oh, The pathname {pathname} was not recognised..."),
        ], fluid=True, className='py-3'
        )
    )