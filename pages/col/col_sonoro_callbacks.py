from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from app import app
from pages.col.col_data import col_dataframe, col_geojson_dataframe
import numpy as np
import math

@app.callback(
    Output('col-map-graph', 'figure'),
    Output('col-table', 'data'),
    Output('col-table', 'columns'),
    Output('z-switch', 'label'),
    [
    Input('lengua-multiselector', 'value'),
    Input('family-multiselector', 'value'),
    Input('depto-multiselector', 'value'),
    Input('hablantes-slider','value'),
    Input('colormap-picker','value'),
    Input('z-switch','checked'),
    Input('legend-switch', 'checked')
    ]
)
def make_col_map(lengua,family, depto, speakers_threshold, colormap,  z_switch, legend_switch):
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
    
    if (z_switch == True):  #(len(col_df['nombre_lengua'].unique()) < 2) or 
        mean = col_df['n_hablantes'].mean() if  len(col_df['nombre_lengua'].unique()) > 2 else 0 
        std = col_df['n_hablantes'].std() if len(col_df['nombre_lengua'].unique()) > 2 else 1
        bubble_size = abs(col_df['n_hablantes'] - mean ) / std
        bubble_max = 45
        legend_title = 'Speakers'
        z_switch_label = "Z Norm"
    elif z_switch == False:
        bubble_size = col_df['lengua_ratio']
        bubble_max = 25  
        legend_title = 'Speakers Ratio'
        z_switch_label = "Speakers Ratio"
    
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
                            col_df['pct_hablantes'], col_df['pct_habitantes'], bubble_size, col_df['lengua_ratio'],
                            col_df['properties.NOMBRE_DPT']
                            ],
                    )
    
    choropleth_col = px.choropleth(
                                col_geojson_,
                                geojson=deptos,
                                locations='properties.DPTO',
                                featureidkey='properties.DPTO',
                                projection='mercator',
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
                        "<I> %{customdata[8]}</I>",
                        "<b> %{customdata[2]} Family</b> - %{customdata[3]}",
                        "<b>Speakers:</b> %{customdata[0]:,} (%Total %{customdata[5]:.2}%)", 
                        "<b>Locals:</b> %{customdata[1]:,} (%Total %{customdata[4]:.2}%)",
                        f"<b>{legend_title}</b>: " + "%{customdata[6]:.2}"
                        ]),
                    marker_sizemin=4
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
        showlegend=legend_switch,
        legend={
            'orientation':'h',
            'font': {'size':14},
            'title':None,
            'xanchor':'left'
        },
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
    return col_fig, col_table.to_dict('records'), table_cols, z_switch_label

@app.callback(
    Output('bubble-legend', 'figure'),
    [
    Input('lengua-multiselector', 'value'),
    Input('family-multiselector', 'value'),
    Input('depto-multiselector', 'value'),
    Input('hablantes-slider','value'),
    Input('colormap-picker','value'),
    Input('z-switch','checked'),
    ]
)
def make_bubble_legend(lengua,family, depto, speakers_threshold, colormap, z_switch):
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
    if (z_switch == True):  #(len(col_df['nombre_lengua'].unique()) < 2) or 
        mean = col_df['n_hablantes'].mean() if  len(col_df['nombre_lengua'].unique()) > 2 else 0 
        std = col_df['n_hablantes'].std() if len(col_df['nombre_lengua'].unique()) > 2 else 1
        bubble_size = abs(col_df['n_hablantes'] - mean ) / std
        bubble_max = 45
        legend_title = 'Speakers'

    elif z_switch == False:
        bubble_size = col_df['lengua_ratio']
        bubble_max = 25  
        legend_title = 'Speakers Ratio'

    ## Bubble Legend Figure
    if bubble_size.max() == bubble_size.min():
        min_bubble = 0
    else:
        min_bubble = bubble_size.min()

    step = round(bubble_size.max() / 3, 1) if bubble_size.max() != bubble_size.min() else bubble_size.max()
    x_array = np.arange(min_bubble, bubble_size.max() * 1.1, step)
    y_array = np.zeros(len(x_array))

    if z_switch:
        text_array = [round((i*std) + mean, -3) if len(col_df['nombre_lengua'].unique()) > 2 else i for i in x_array]
    else:
        text_array = x_array


    bubble_fig = px.scatter(
                            x = x_array,
                            y = y_array,
                            size = x_array,
                            size_max=bubble_max,
                            color_discrete_sequence=['black'],
                            height=150,
                            text=[f'{size_:.0%}' if not z_switch else f'{size_:,.1f}'.strip("0")  for size_ in text_array]
                        )
    bubble_fig.update_traces(
                            hovertemplate=None, 
                            hoverinfo='skip', 
                            textposition='bottom center',
                            marker_sizemin=4
                            )
    bubble_fig.update_layout(
                            title=dict(text=legend_title, x=0., y=0.8),
                            xaxis=dict(showgrid=False, visible=False),
                            yaxis=dict(showgrid=False, visible=False),
                            margin=dict(t=0,b=0,l=20,r=250),
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
        title={'text': "Total Speakers", 'font':{'size':15}},
        )
    trace2 = go.Indicator(
        mode="number",    
        value=col_df.nombre_lengua.nunique(),    
        domain={'x': [0.33, 0.66], 'y': [0., 1.]},  
        number={'font':{'size':35}},  
        title={'text': "Languages", 'font':{'size':15}})
    trace3 = go.Indicator(
        mode="number",    
        value=col_df.n_habitantes.sum(),    
        domain={'x': [0.66, 1.0], 'y': [0., 1.00]},  
        number={'valueformat':',r', 'font':{'size':35}}, 
        title={'text': "Total Locals", 'font':{'size':15}})

    # layout and figure production
    layout = go.Layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis={'showgrid': False, 'showticklabels':False, 'range':[-1,1]},
                    yaxis={'showgrid': False, 'showticklabels':False, 'range':[0,1]},
                    margin=dict(l=20, r=20, t=20, b=20),
                    autosize=True,
                    #height=100
                    )
    fig = go.Figure(data = [trace1, trace2, trace3], layout = layout)
    fig.add_annotation(
                text='out of <b>48,258,494</b> colombians <I>(DANE, 2018 Census)</I>',
                x=0.2,
                y=0.1,
                xref='x',
                yref='y',
                showarrow=False,
    )

    return fig

@app.callback(
    Output('stats-section', 'style'),
    [
    Input('stats-switch', 'checked'),
    ]
)
def display_stats_page(hide_switch):
    '''
        Shows/Hides Stats Section
    '''
    if hide_switch:
        return {'display':'block'}
    else:
        return {'display':'none'}

'''
   Here your callback functions
'''

# "Most Endangered Native Languages in Colombia (Linguistic Family)" Plot
@app.callback(
    Output(component_id='family-endangered-plot', component_property='figure'),
    [
    Input(component_id='stats-switch', component_property='checked')
    ]
)
def update_endangered_plot(stats_switch):
    ''' returns horizontal bar figure with most endangered languages in Colombia
    '''
    col_df = col_dataframe()
    endangered_df = col_df[(col_df['vitalidad'] == 'Critically Endangered')][['familia_linguistica', 'nombre_lengua','n_hablantes','n_habitantes']].\
        groupby(['nombre_lengua', 'familia_linguistica']).agg({'n_hablantes':'sum','n_habitantes':'sum'}).\
        sort_values(by=['n_habitantes'], ascending=False).reset_index()
    endangered_df = endangered_df.assign(endangered_ratio=1-(endangered_df.n_hablantes/endangered_df.n_habitantes))
    endangered_df = endangered_df.sort_values(by=['endangered_ratio', 'n_hablantes', 'n_habitantes'], ascending=[False, True, True]).reset_index()
    endangered_df = endangered_df.head(11)
    endangered_df = endangered_df.assign(bar_color='rgba(158, 160, 170, 0.6)')
    endangered_df['bar_color'][0:5] = '#8daad6'

    subplots = make_subplots(
        rows=len(endangered_df['endangered_ratio']),
        cols=1,
        subplot_titles=[x for x in endangered_df['nombre_lengua']],
        shared_xaxes=True,
        print_grid=False,
        vertical_spacing=(0.45 / len(endangered_df['endangered_ratio'])),
    )
    subplots['layout'].update(
        plot_bgcolor='#fff',
    )
    # add bars for the categories
    for k,x in enumerate(endangered_df['nombre_lengua']):
        subplots.add_trace(dict(
            type='bar',
            orientation='h',
            y=[x],
            x=[endangered_df['endangered_ratio'][k]],
            text=["{:,.0f} speakers out of {:,.0f} locals".format(endangered_df["n_hablantes"][k],endangered_df['n_habitantes'][k])],
            hoverinfo='text',
            textposition='auto',
            textfont_color='white',
            marker=dict(color=endangered_df['bar_color'][k],),
        ), k+1, 1)

    # update the layout
    subplots['layout'].update(
        showlegend=False,
    )
    for x in subplots["layout"]['annotations']:
        x['x'] = 0
        x['xanchor'] = 'left'
        x['align'] = 'left'
        x['font'] = dict(size=14, )

    # hide the axes
    for axis in subplots['layout']:
        if axis.startswith('yaxis') or axis.startswith('xaxis'):
            subplots['layout'][axis]['visible'] = False

    # update the margins and size
    subplots['layout']['margin'] = {
        'l': 0,
        'r': 0,
        't': 20,
        'b': 5,
    }

    return subplots