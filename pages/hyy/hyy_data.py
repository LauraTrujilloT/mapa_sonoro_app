'''
Decaimiento HYY
extraído de ATLAS Open Data
'''
from utils.hyy_functions import *
from utils.constants import TIMEOUT
from app import cache
import pandas as pd

# Data Sample A
# Constants
lumi = 0.5 #fb-1
fraction = 0.8
data_path = "https://raw.githubusercontent.com/LauraTrujilloT/notebooks-collection-opendata-dashapp/dev-dash/data_extracts/13TeV/hyy_data_sample_a.csv"
sample_list = ['sample_A']
 
@cache.memoize(timeout=TIMEOUT)
def hyy_dataframe():
    return pd.read_csv(data_path)