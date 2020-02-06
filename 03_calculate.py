import pandas as pd
import numpy as np
from tqdm import tqdm
from utils.data import mdage
from utils.get_median import get_median
import math
import json

df = pd.read_csv('data/intermediate.csv', index_col=False, low_memory=False)
lookup = json.load(open('data/variable_lookup.json'))
var = list(lookup.keys())
for i in tqdm(var):
    base_variables = lookup[i]
    df[i] = np.apply_along_axis(sum, 1, df.loc[:, base_variables])

# special cases:
# df['PopPerAcre'] = df['Pop1']/df['LandAcres'] #need landacres first
special_var = ['OAsnAlone', 'AsnInCombo', 'OthrRel', 'AvgHHSz', 
                'PopInFam', 'AvgFamSz', 'HmOwnrVcRt', 'RntVcRt',
                'AvHHSzOOc', 'AvHHSzROc', 'mdage']

df['OAsnAlone'] = df['AsnAlone']-df['AsnInd']-df['Bgldsh']\
                    - df['Cambdn']-df['Chinese']-df['Filipino']\
                    - df['Indonsn']-df['Japanese']-df['Korean']\
                    - df['Mlysn']-df['Pak']-df['SLkn']-df['Thai']-df['Vietnms']

df['AsnInCombo'] = df['AsnAlnOrC']-df['AsnAlone']

df['OthrRel'] = df['PopInFHH']-df['HHldr']-df['Spouse']-df['OwnCU18']-df['NonRel']

# df['AvgHHSz'] = df['PopInHH']/df['OccHU1']
df['AvgHHSz'] = df['PopInHH']/df['OOcHU1']

df['PopInFam'] = df['PopInFHH']-df['NonRel']

df['AvgFamSz'] = df['PopInFam']/df['Fam1']

df['HmOwnrVcRt'] = df['VHUFSlO']*100/(df['OOcHU1']+df['VHUFSlO'])

df['RntVcRt'] = df['VHUFRnt']*100/(df['ROcHU_3']+df['VHUFRnt'])

df['AvHHSzOOc'] = df['PopOOcHU']/df['OOcHU']

df['AvHHSzROc'] = df['PopROcHU']/df['ROcHU_1']

df['mdage'] = df.apply(lambda row: get_median(mdage, row), axis=1)

df.to_csv(f'data/intermediate_calculated.csv', index=False,
            columns =['state', 'place', 'county', 'tract', 'block', 
                    'geotype', 'nta_code', 'puma']+var+special_var)

