'''
Any query to Mapa Sonoro Colombia Data is done here
@lvtrujillot
'''
from utils.constants import TIMEOUT
from app import cache
import pandas as pd
import json

# Data Sample 
col_data_path = "data/colombia_sonoro_app.csv"
col_geojson_path ="data/colombia.json"

@cache.memoize(timeout=TIMEOUT)
def col_dataframe():
    col_df = pd.read_csv(col_data_path)
    col_df['vitalidad'] = col_df['vitalidad'].replace(['En peligro'],'Critically Endangered')
    col_df['vitalidad'] = col_df['vitalidad'].replace(['En peligro de extinción'], 'Critically Endangered')
    col_df['vitalidad'] = col_df['vitalidad'].replace(['Vulnerable','En situación critica'], 'Vulnerable')
    return col_df

@cache.memoize(timeout=TIMEOUT)
def col_geojson_dataframe():
    with open(col_geojson_path) as response:
        deptos = json.load(response)
    ## Colombia
    col_geojson = pd.json_normalize(deptos['features'])
    col_geojson = col_geojson.assign(pais='Colombia')
    return col_geojson, deptos


