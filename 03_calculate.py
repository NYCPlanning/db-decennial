import pandas as pd
import numpy as np
import tqdm
import math
import json

df = pd.read_csv('data/intermediate.csv', index_col=False, low_memory=False)
lookup = json.load(open('data/variable_lookup.json'))
var = list(lookup.keys())
for i in tqdm(var):
    base_variables = lookup[i]
    df[i] = np.apply_along_axis(sum, 1, df.loc[:, base_variables])

df.to_csv(f'data/intermediate_calculated.csv', index=False,
            columns =['state', 'place', 'county', 'tract', 'block', 
                    'geotype', 'nta_code', 'puma']+var)
