'''
Any query to Mapa Sonoro Colombia Data is done here
@lvtrujillot
'''
from utils.constants import TIMEOUT
from app import cache
import pandas as pd

# Data Sample 
data_path = ""

 
@cache.memoize(timeout=TIMEOUT)
def col_dataframe():
    return pd.read_csv(data_path)