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
    Input('test-switch', 'checked'),
    Input('family-multiselector', 'value'),
    Input('depto-multiselector', 'value')
    ]
)
def make_col_map(checked, family, depto):
    '''
    '''
    col_geojson_, deptos = col_geojson_dataframe()
    if checked:
        col_df = col_dataframe()
    else:
        col_df = col_dataframe()
    if family:
        col_df = col_df[col_df['familia_linguistica'].isin(family)]
    if depto:
        col_df = col_df[col_df['departamento'].isin(depto)]
        col_geojson_ = col_geojson_[col_geojson_['properties.NOMBRE_DPT'].isin(depto)]
 
    mean = col_df['n_hablantes'].mean()
    std = col_df['n_hablantes'].std()
    
    col_fig = px.scatter_mapbox(
                        col_df.dropna(), 
                        lat=col_df["municipio_latitud"].astype(float), 
                        lon=col_df["municipio_longitud"].astype(float),     
                        color=col_df["vitalidad"], 
                        size=abs(col_df['n_hablantes'] - mean ) / std,
                        mapbox_style='carto-positron',
                        size_max=45,
                        zoom=5,
                        height=900,
                        center = {"lat": 4.7110, "lon": -74.0421},
                        color_discrete_map={
                                            'En peligro':'#DC3535',
                                            'En peligro de extinción':'#DC3535',
                                            'Vulnerable':'#FFE15D',
                                            'En situación crtica':'#F49D1A'
                                    }
                        )
     
    choropleth_col = px.choropleth_mapbox(
                            col_geojson_, 
                            geojson=deptos, 
                            featureidkey='properties.DPTO',
                            locations='properties.DPTO', 
                            mapbox_style="carto-positron",
                            zoom=5, 
                            center = {"lat": 4.7110, "lon": -74.0421},
                            opacity=0.55,
                            #width=700,
                            height=900,
                            color_discrete_sequence=['#B2B2B2']
                          )
    col_fig.add_trace(choropleth_col.data[0])
    for i, frame in enumerate(col_fig.frames):
        col_fig.frames[i].data += (choropleth_col.frames[i].data[0],)

    col_fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}, 
        #margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False)

    col_table = col_df[['departamento', 'nombre_lengua','vitalidad', 'n_hablantes','n_habitantes']].\
        sort_values(['departamento','nombre_lengua'], ascending=(True,True))
    col_table['departamento'] = col_table['departamento'].str.capitalize()
    col_table.rename(columns={'n_hablantes':'Hablantes', 'n_habitantes':'Habitantes'},inplace=True)
    table_cols = [{'name':i.replace('_', ' ').capitalize(), 'id':i} for i in col_table.columns]
    return col_fig, col_table.to_dict('records'), table_cols

@app.callback(
    Output('hablantes-indicator', 'figure'),
    #Output('habitantes-indicator', 'figure'),
    #Output('lenguas-indicator', 'figure'),
    [
    Input('test-switch', 'checked'),
    Input('family-multiselector', 'value'),
    Input('depto-multiselector', 'value')
    ]
)
def update_indicators(checked, family, depto):
    '''
    '''
    col_df = col_dataframe()

    trace1 = go.Indicator(
        mode="number",    
        value=col_df.n_hablantes.sum(),    
        domain={'x': [0., 0.33], 'y': [0.0, 1.]},  
        number={'valueformat':',r', 'font':{'size':35}},  
        title={'text': "Total Hablantes", 'font':{'size':15}})
    trace2 = go.Indicator(
        mode="number",    
        value=col_df.nombre_lengua.count(),    
        domain={'x': [0.33, 0.66], 'y': [0., 1.]},  
        number={'font':{'size':35}},  
        title={'text': "Total Lenguas", 'font':{'size':15}})
    trace3 = go.Indicator(
        mode="number",    
        value=col_df.n_habitantes.sum(),    
        domain={'x': [0.66, 1.0], 'y': [0., 1.00]},  
        number={'valueformat':',r', 'font':{'size':35}}, 
        title={'text': "Total Habitantes", 'font':{'size':15}})

    # layout and figure production
    layout = go.Layout(
                    #paper_bgcolor='rgb(0,0,0)',
                    margin=dict(l=20, r=20, t=20, b=20),
                    autosize=False,
                    )
    fig = go.Figure(data = [trace1, trace2, trace3], layout = layout)

    return fig