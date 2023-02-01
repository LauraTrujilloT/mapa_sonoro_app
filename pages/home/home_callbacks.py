from dash.dependencies import Input, Output
import plotly.express as px
from app import app
from pages.col.col_data import col_dataframe, col_geojson_dataframe
import numpy as np
import plotly.figure_factory as ff

def make_col_map_home():
    '''
    Return Plotly figure map of Colombia
    '''
    col_geojson_, deptos = col_geojson_dataframe()
    col_df = col_dataframe()
    speakers_total = col_df['n_hablantes'].sum()
    locals_total = col_df['n_habitantes'].sum()
    col_df['pct_hablantes'] = (col_df['n_hablantes'] * 100) / speakers_total
    col_df['pct_habitantes'] = (col_df['n_habitantes'] * 100) / locals_total

    choropleth_col = px.choropleth_mapbox(
                                col_geojson_,
                                geojson=deptos,
                                locations='properties.DPTO',
                                featureidkey='properties.DPTO',
                                mapbox_style="white-bg",
                                zoom=5.2, 
                                center = {"lat": 4, "lon": -73.0421},
                                opacity=.6,
                                color_discrete_sequence=['black']#['#2781A5']
                            )

    choropleth_col.update_traces(
        hoverinfo='skip',
        hovertemplate=None,
        marker_line_width=0.8,
        marker_line_color='#FFEA20')
    choropleth_col.update_geos(fitbounds='locations',visible=False)

    choropleth_col.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}, 
        showlegend=False,
        hoverlabel={
            'font':{'size':15},
            'bgcolor':'rgba(255,255,255,0.75)'
            },
        paper_bgcolor='#f8f9fa'
        )
    return choropleth_col