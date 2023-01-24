from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from app import app
from pages.col.col_data import col_dataframe, col_geojson_dataframe
import numpy as np

@app.callback(
    Output('col-map-graph', 'figure'),
    Output('col-table', 'data'),
    Output('col-table', 'columns'),
    [
    Input('lengua-multiselector', 'value'),
    Input('family-multiselector', 'value'),
    Input('depto-multiselector', 'value'),
    Input('hablantes-slider','value'),
    Input('colormap-picker','value'),
    Input('carto-switch', 'checked'),
    Input('z-switch','checked'),
    ]
)
def make_col_map(lengua,family, depto, speakers_threshold, colormap, show_stats, z_switch):
    '''
    Return Plotly figure (map + scatter)
    '''
    col_geojson_, deptos = col_geojson_dataframe()
    col_df = col_dataframe()
    speakers_total = col_df['n_hablantes'].sum()
    locals_total = col_df['n_habitantes'].sum()
    col_df['pct_hablantes'] = (col_df['n_hablantes'] * 100) / speakers_total
    col_df['pct_habitantes'] = (col_df['n_habitantes'] * 100) / locals_total
    if lengua:
        col_df = col_df[col_df['nombre_lengua'].isin(lengua)]
    if family:
        col_df = col_df[col_df['familia_linguistica'].isin(family)]
    if depto:
        col_df = col_df[col_df['departamento'].isin(depto)]
        col_geojson_ = col_geojson_[col_geojson_['properties.NOMBRE_DPT'].isin(depto)]
    if speakers_threshold:
        col_df = col_df[col_df['n_hablantes'] <= speakers_threshold]
    if not colormap:
        colormap = 'rgb(226,233, 244)'
    if not show_stats:
        show_stats =  True
    else:
        show_stats = False
    
    if (len(col_df['nombre_lengua'].unique()) < 2) or (z_switch == True) :
        mean = col_df['n_hablantes'].mean()
        std = col_df['n_hablantes'].std() 
        bubble_size = abs(col_df['n_hablantes'] - mean ) / std
        bubble_max = 45
    elif z_switch == False:
        bubble_size = col_df['lengua_ratio']
        bubble_max = 25  
    
    col_fig = px.scatter_geo(
                        col_df.dropna(), 
                        lat=col_df["municipio_latitud"].astype(float), 
                        lon=col_df["municipio_longitud"].astype(float),     
                        color=col_df["vitalidad"], 
                        size=bubble_size,
                        size_max=bubble_max,
                        height=1000,
                        center = {"lat": 4.0, "lon": -72.5},
                        opacity=1.,
                        scope='south america',
                        color_discrete_map={
                                            'Critically Endangered':'#A90639',#'rgb(250, 87, 98)',
                                            'Endangered': '#e60049',#'#96dae8'
                                            'Vulnerable': '#FFE15D',#'#FFF600',#'#FFE15D',
                                    },
                        custom_data=[col_df["n_hablantes"], col_df['n_habitantes'], 
                            col_df['familia_linguistica'], col_df['nombre_lengua'],
                            col_df['pct_hablantes'], col_df['pct_habitantes']
                            ],
                    )
    
    choropleth_col = px.choropleth(
                                col_geojson_,
                                geojson=deptos,
                                locations='properties.DPTO',
                                featureidkey='properties.DPTO',
                                #projection='mercator',
                                height=1000,
                                color_discrete_sequence=[colormap]
                            )
    choropleth_col.update_traces(
        hoverinfo='skip',
        hovertemplate=None,
        marker_line_width=0.5,
        marker_line_color='#8daad6')
    choropleth_col.update_geos(fitbounds='locations',visible=False)
    col_fig.update_geos(fitbounds='locations', visible=False, bgcolor='#f8f9fa')

    col_fig.update_traces(
                    hovertemplate="<br>".join([
                        "<b> %{customdata[2]} Family</b> - %{customdata[3]}",
                        "<b>Speakers:</b> %{customdata[0]:,}",
                        "<b>%Speakers:</b> %{customdata[5]:.2}%", 
                        "<b>Locals:</b> %{customdata[1]:,}",
                        "<b>%Locals</b> %{customdata[4]:.2}%",
                        ])
    )
    col_fig.add_trace(choropleth_col.data[0])
    for i, frame in enumerate(col_fig.frames):
        col_fig.frames[i].data += (choropleth_col.frames[i].data[0],)

    col_fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}, 
        title={
            'text': 'Colombia Map',
            'x':0.2,
            'y':0.98,
            'xanchor':'center'
            },
        showlegend=True,
        hoverlabel={
            'font':{'size':15},
            'bgcolor':'rgba(255,255,255,0.75)'
            },
        paper_bgcolor='#f8f9fa'
        )

    col_table = col_df[['departamento', 'nombre_lengua','vitalidad']].\
        sort_values(['departamento','nombre_lengua'], ascending=(True,True))
    col_table['departamento'] = col_table['departamento'].str.capitalize()
    col_table.rename(columns={'departamento':'State', 'nombre_lengua':'Language', 'Vitalidad':'Status'},inplace=True)
    table_cols = [{'name':i.replace('_', ' ').capitalize(), 'id':i} for i in col_table.columns]
    return col_fig, col_table.to_dict('records'), table_cols

@app.callback(
    Output('bubble-legend', 'figure'),
    [
    Input('lengua-multiselector', 'value'),
    Input('family-multiselector', 'value'),
    Input('depto-multiselector', 'value'),
    Input('hablantes-slider','value'),
    Input('colormap-picker','value'),
    Input('carto-switch', 'checked'),
    Input('z-switch','checked'),
    ]
)
def make_bubble_legend(lengua,family, depto, speakers_threshold, colormap, show_stats, z_switch):
    '''
    Return Plotly figure for Bubble legend
    '''
    col_geojson_, deptos = col_geojson_dataframe()
    col_df = col_dataframe()
    speakers_total = col_df['n_hablantes'].sum()
    locals_total = col_df['n_habitantes'].sum()
    col_df['pct_hablantes'] = (col_df['n_hablantes'] * 100) / speakers_total
    col_df['pct_habitantes'] = (col_df['n_habitantes'] * 100) / locals_total
    if lengua:
        col_df = col_df[col_df['nombre_lengua'].isin(lengua)]
    if family:
        col_df = col_df[col_df['familia_linguistica'].isin(family)]
    if depto:
        col_df = col_df[col_df['departamento'].isin(depto)]
        col_geojson_ = col_geojson_[col_geojson_['properties.NOMBRE_DPT'].isin(depto)]
    if speakers_threshold:
        col_df = col_df[col_df['n_hablantes'] <= speakers_threshold]
    if not colormap:
        colormap = 'rgb(226,233, 244)'
    if not show_stats:
        show_stats =  True
    else:
        show_stats = False
    
    if (len(col_df['nombre_lengua'].unique()) < 2) or (z_switch == True) :
        mean = col_df['n_hablantes'].mean()
        std = col_df['n_hablantes'].std() 
        bubble_size = abs(col_df['n_hablantes'] - mean ) / std
        bubble_max = 45
        legend_title = 'Speakers'
    elif z_switch == False:
        bubble_size = col_df['lengua_ratio']
        bubble_max = 25  
        legend_title = 'Speakers Ratio'

    ## Bubble Legend Figure
    
    step = round(bubble_size.max() / 3, 1)
    x_array = np.arange(bubble_size.min(), bubble_size.max(), step)
    y_array = np.zeros(len(x_array))
    if z_switch:
        text_array = [round((i*std) + mean, -3) for i in x_array]
    else:
        text_array = x_array


    bubble_fig = px.scatter(
                            x = x_array,
                            y = y_array,
                            size = x_array,
                            size_max=bubble_max,
                            color_discrete_sequence=['black'],
                            height=150,
                            text=[f'{size_:.0%}' if not z_switch else f'{size_:.0f}'.strip("0") + 'K' for size_ in text_array]
                        )
    bubble_fig.update_traces(
                            hovertemplate=None, 
                            hoverinfo='skip', 
                            textposition='bottom center',
                            )
    bubble_fig.update_layout(
                            title=dict(text=legend_title, x=0.1, y=0.5),
                            xaxis=dict(showgrid=False, visible=False),
                            yaxis=dict(showgrid=False, visible=False),
                            margin=dict(t=0,b=0,l=250,r=0),
                            paper_bgcolor='#f8f9fa',
                            plot_bgcolor='#f8f9fa'
                        )

    return bubble_fig

@app.callback(
    Output('hablantes-indicator', 'figure'),
    #Output('habitantes-indicator', 'figure'),
    #Output('lenguas-indicator', 'figure'),
    [
    Input('family-multiselector', 'value'),
    Input('depto-multiselector', 'value')
    ]
)
def update_indicators(family, depto):
    '''
    Returns KPIs
    '''
    col_df = col_dataframe()

    trace1 = go.Indicator(
        mode="number",    
        value=col_df.n_hablantes.sum(),    
        domain={'x': [0., 0.33], 'y': [0.0, 1.]},  
        number={'valueformat':',r', 'font':{'size':35}},  
        title={'text': "Speakers", 'font':{'size':15}})
    trace2 = go.Indicator(
        mode="number",    
        value=col_df.nombre_lengua.nunique(),    
        domain={'x': [0.33, 0.66], 'y': [0., 1.]},  
        number={'font':{'size':35}},  
        title={'text': "Native Languages", 'font':{'size':15}})
    trace3 = go.Indicator(
        mode="number",    
        value=col_df.n_habitantes.sum(),    
        domain={'x': [0.66, 1.0], 'y': [0., 1.00]},  
        number={'valueformat':',r', 'font':{'size':35}}, 
        title={'text': "Locals", 'font':{'size':15}})

    # layout and figure production
    layout = go.Layout(
                    #paper_bgcolor='rgb(0,0,0)',
                    margin=dict(l=20, r=20, t=20, b=20),
                    autosize=True,
                    #height=100
                    )
    fig = go.Figure(data = [trace1, trace2, trace3], layout = layout)

    return fig