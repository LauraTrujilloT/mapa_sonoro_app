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
    return pd.read_csv(col_data_path)

@cache.memoize(timeout=TIMEOUT)
def col_geojson_dataframe():
    with open(col_geojson_path) as response:
        deptos = json.load(response)
    ## Colombia
    col_geojson = pd.json_normalize(deptos['features'])
    col_geojson = col_geojson.assign(pais='Colombia')
    return col_geojson, deptos
