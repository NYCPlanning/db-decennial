import pandas as pd
import numpy as np
from tqdm import tqdm
from utils.data import mdage
from utils.get_median import get_median
import math
import json

df = pd.read_csv('data/intermediate.csv', index_col=False, low_memory=False)
landarea = pd.read_excel('data/Decennial/Land Area for Decennial Profile.xlsx')
landarea = landarea.loc[landarea.Year==2010, :]
lookup = json.load(open('data/variable_lookup.json'))
var = list(lookup.keys())
for i in tqdm(var):
    base_variables = lookup[i]
    df[i] = np.apply_along_axis(sum, 1, df.loc[:, base_variables])

# special cases:
df = pd.merge(df, landarea[['GeoID', 'LandAcres']], 
                how='left', left_on='geoid', right_on='GeoID')

df['PopPerAcre'] = df['Pop1']/df['LandAcres'] #need landacres first

df['OAsnAlone'] = df['AsnAlone']-df['AsnInd']-df['Bgldsh']\
                    - df['Cambdn']-df['Chinese']-df['Filipino']\
                    - df['Indonsn']-df['Japanese']-df['Korean']\
                    - df['Mlysn']-df['Pak']-df['SLkn']\
                    -df['Thai']-df['Vietnms']

df['AsnInCombo'] = df['AsnAlnOrC']-df['AsnAlone']

df['OthrRel'] = df['PopInFHH']-df['HHldr']-df['Spouse']\
                -df['OwnCU18']-df['NonRel']

df['AvgHHSz'] = df['PopInHH']/df['OcHU_1']

df['PopInFam'] = df['PopInFHH']-df['NonRel']

df['AvgFamSz'] = df['PopInFam']/df['Fam1']

df['HmOwnrVcRt'] = df['VHUFSlO']*100/(df['OOcHU1']+df['VHUFSlO'])

df['RntVcRt'] = df['VHUFRnt']*100/(df['ROcHU_3']+df['VHUFRnt'])

df['AvHHSzOOc'] = df['PopOOcHU']/df['OOcHU']

df['AvHHSzROc'] = df['PopROcHU']/df['ROcHU_1']

df['MdAge'] = df.apply(lambda row: get_median(mdage, row), axis=1)

special_var = ['OAsnAlone', 'AsnInCombo', 'OthrRel', 
                'AvgHHSz', 'PopInFam', 'AvgFamSz', 
                'HmOwnrVcRt', 'RntVcRt','AvHHSzOOc', 
                'AvHHSzROc', 'MdAge', 'LandAcres', 
                'PopPerAcre']

df.to_csv('data/intermediate_calculated.csv', index=False,
            columns =['geoid']+var+special_var)

