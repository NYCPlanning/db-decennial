import pandas as pd
import math
import numpy as np
from utils.data import names

df = pd.read_csv(f'data/raw.csv', index_col=False, dtype='str')
dff = df[df.geotype=='CT2010']
# dff = dff.fillna(0)
for i in names:
    dff[i] = dff[i].astype(int)

nta = pd.read_excel('data/nyc2010census_tabulation_equiv.xlsx',
                    skiprows=4, dtype=str,
                    names=['borough', 'fips', 'borough_code', 
                            'tract', 'puma', 'nta_code', 'nta_name'])

dff = pd.merge(nta[['nta_code', 'puma', 'fips', 'tract']], dff, how='left', left_on=['fips','tract'], right_on=['county','tract'])
nta_df = dff.groupby(['nta_code'], as_index=False).sum()
nta_df['geotype'] = 'NTA2010'
puma_df = dff.groupby(['puma'], as_index=False).sum()
puma_df['geotype'] = 'PUMA2010'

df = pd.concat([df, nta_df, puma_df], sort=True)
df.to_csv('data/intermediate.csv', index=False,
            columns=['state', 'place', 'county', 'tract', 'block', 
                    'geotype', 'nta_code', 'puma']+names)