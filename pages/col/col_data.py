'''
Any query to Mapa Sonoro Colombia Data is done here
@lvtrujillot
'''
from utils.constants import TIMEOUT
from app import cache
import pandas as pd

# Data Sample 
data_path = "https://raw.githubusercontent.com/LauraTrujilloT/mapa_sonoro_app/main/data/colombia_sonoro_app.csv?token=GHSAT0AAAAAAB5B7FDXUE3YWCVBD4WI2FHIY5ZZDAQ"

@cache.memoize(timeout=TIMEOUT)
def col_dataframe():
    return pd.read_csv(data_path)