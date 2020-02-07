import pandas as pd
import json
import numpy as np
from tqdm import tqdm
from utils.data import special_var, rounding
YEAR = '2010'
lookup = json.load(open('data/variable_lookup.json'))
var = list(lookup.keys())+special_var
df = pd.read_csv(f'data/intermediate_calculated.csv', index_col=False)

r = []
for i in tqdm(var):
    dff = df.loc[:,['geoid', i]].reindex()
    dff.columns=['geoid', 'value']
    try:
        dff.loc[:, 'value'] = dff['value'].round(rounding.get(i))
    except: 
        dff.loc[:, 'value'] = dff['value']
    dff.loc[:, 'variable'] = i
    dff.loc[:, 'year'] = YEAR
    r.append(dff)
result = pd.concat(r)
result.to_csv(f'data/final.csv', index=False)