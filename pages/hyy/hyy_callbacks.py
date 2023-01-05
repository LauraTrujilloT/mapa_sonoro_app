from dash.dependencies import Input, Output
import plotly.express as px
from app import app
from utils.hyy_functions import *
from pages.hyy.hyy_data import hyy_dataframe


@app.callback(
    Output('hyy-graph', 'srcDoc'),
    Input('hyy-variable', 'value'))
def update_figure(selected_value):
    hyy_df = hyy_dataframe()
    filtered_df = hyy_df[hyy_df.myy == selected_value]
    html_fig = plot_data(data=hyy_df)
    return html_fig