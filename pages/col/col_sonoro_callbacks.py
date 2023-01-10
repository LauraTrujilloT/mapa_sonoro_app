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
                        height=700,
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
                            width=700,
                            height=800,
                            color_discrete_sequence=['#B2B2B2']
                          )
    col_fig.add_trace(choropleth_col.data[0])
    for i, frame in enumerate(col_fig.frames):
        col_fig.frames[i].data += (choropleth_col.frames[i].data[0],)
    col_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, showlegend=False)

    col_table = col_df[['departamento', 'nombre_lengua','vitalidad', 'n_hablantes','n_habitantes']].\
        sort_values(['departamento','nombre_lengua'], ascending=(True,True))
    col_table['departamento'] = col_table['departamento'].str.capitalize()
    col_table.rename(columns={'n_hablantes':'Hablantes', 'n_habitantes':'Habitantes'},inplace=True)
    table_cols = [{'name':i.replace('_', ' ').capitalize(), 'id':i} for i in col_table.columns]
    return col_fig, col_table.to_dict('records'), table_cols