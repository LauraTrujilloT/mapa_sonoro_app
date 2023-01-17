from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from app import app
from pages.col.col_data import col_dataframe, col_geojson_dataframe

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
def make_col_map(lengua,family, depto, speakers_threshold, colormap, show_carto, z_switch):
    '''
    '''
    col_geojson_, deptos = col_geojson_dataframe()
    col_df = col_dataframe()
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
        colormap = 'rgba(19, 32, 56, 1)'
    if not show_carto:
        show_carto = 'white-bg'
    else:
        show_carto = 'carto-positron'
    
    if (len(col_df['nombre_lengua'].unique()) < 2) or (z_switch == True) :
        mean = col_df['n_hablantes'].mean()
        std = col_df['n_hablantes'].std() 
        bubble_size = abs(col_df['n_hablantes'] - mean ) / std
        bubble_max = 45
    elif z_switch == False:
        bubble_size = col_df['lengua_ratio']
        bubble_max = 15   
    
    col_fig = px.scatter_mapbox(
                        col_df.dropna(), 
                        lat=col_df["municipio_latitud"].astype(float), 
                        lon=col_df["municipio_longitud"].astype(float),     
                        color=col_df["vitalidad"], 
                        size=bubble_size,
                        mapbox_style=show_carto,#'carto-positron',
                        size_max=bubble_max,
                        zoom=5,
                        height=900,
                        center = {"lat": 4.0, "lon": -72.5},
                        opacity=1,
                        color_discrete_map={
                                            'Critically Endangered':'rgb(271, 71, 130)',
                                            'Vulnerable':'#FFE15D',
                                            'Endangered':'rgb(227,137,56)'
                                    },
                        custom_data=[col_df["n_hablantes"], col_df['n_habitantes'], 
                            col_df['familia_linguistica'], col_df['nombre_lengua']],
                        )
     
    choropleth_col = px.choropleth_mapbox(
                            col_geojson_, 
                            geojson=deptos, 
                            featureidkey='properties.DPTO',
                            locations='properties.DPTO', 
                            mapbox_style=show_carto,#"carto-positron",
                            zoom=5, 
                            center = {"lat": 4.0, "lon": -72.5},
                            opacity=1.,
                            height=900,
                            color_discrete_sequence=[colormap]#['#B2B2B2']
                          )
    choropleth_col.update_traces(
        hoverinfo='skip',
        hovertemplate=None,
        marker_line_width=0.1,
        marker_line_color='white')
    col_fig.update_traces(
    hovertemplate="<br>".join([
        #"ColX: %{x}",
        #"ColY: %{y}",
        "<b> %{customdata[2]} Family</b> - %{customdata[3]}",
        "<b>Speakers:</b> %{customdata[0]:,}",
        "<b>Locals:</b> %{customdata[1]:,}",
        #"Col3: %{customdata[2]}",
        ])
    )
    col_fig.add_trace(choropleth_col.data[0])
    for i, frame in enumerate(col_fig.frames):
        col_fig.frames[i].data += (choropleth_col.frames[i].data[0],)

    col_fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}, 
        showlegend=False,
        hoverlabel={'font':{'size':15}})

    col_table = col_df[['departamento', 'nombre_lengua','vitalidad']].\
        sort_values(['departamento','nombre_lengua'], ascending=(True,True))
    col_table['departamento'] = col_table['departamento'].str.capitalize()
    col_table.rename(columns={'departamento':'State', 'nombre_lengua':'Language', 'Vitalidad':'Status'},inplace=True)
    table_cols = [{'name':i.replace('_', ' ').capitalize(), 'id':i} for i in col_table.columns]
    return col_fig, col_table.to_dict('records'), table_cols

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
        value=col_df.nombre_lengua.count(),    
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