from multiprocessing import Pool, cpu_count
import requests
import pandas as pd
import numpy as np
import json
import os
from utils.data import names

api_key=os.environ['API_KEY']
# tracts: 
i = 0
tables = []
while i < len(names):
    begin = i
    end = i+50 if i+50 < len(names) else len(names)
    r = json.loads(requests.get(f'https://api.census.gov/data/2010/dec/sf1?get={",".join(names[begin:end])}&for=tract:*&in=state:36&in=county:081,085,005,047,061&key={api_key}').content)
    df = pd.DataFrame(r[1:])
    df.columns = r[0]
    tables.append(df)
    i += 50

df_tract = pd.concat(tables, axis=1, sort=False)
df_tract = df_tract.loc[:,~df_tract.columns.duplicated()]
df_tract['geotype'] = 'CT2010'
print('tract level complete ...')

# block: 
i = 0
tables = []
while i < len(names):
    begin = i
    end = i+50 if i+50 < len(names) else len(names)
    tract_tables = []
    for county in ['081','085','005','047','061']:
        r = json.loads(requests.get(f'https://api.census.gov/data/2010/dec/sf1?get={",".join(names[begin:end])}&for=block:*&in=state:36&in=county:{county}&in=tract:*&key={api_key}').content)
        df = pd.DataFrame(r[1:])
        df.columns = r[0]
        tract_tables.append(df)
    df = pd.concat(tract_tables)
    tables.append(df)
    i += 50

df_block = pd.concat(tables, axis=1, sort=False)
df_block = df_block.loc[:,~df_block.columns.duplicated()]
df_block['geotype'] = 'CB2010'
print('block level complete ...')

# county/boro
i = 0
tables = []
while i < len(names):
    begin = i
    end = i+50 if i+50 < len(names) else len(names)
    r = json.loads(requests.get(f'https://api.census.gov/data/2010/dec/sf1?get={",".join(names[begin:end])}&for=county:081,085,005,047,061&in=state:36&key={api_key}').content)
    df = pd.DataFrame(r[1:])
    df.columns = r[0]
    tables.append(df)
    i += 50

df_boro = pd.concat(tables, axis=1, sort=False)
df_boro = df_boro.loc[:,~df_boro.columns.duplicated()]
df_boro['geotype'] = 'Boro2010'
print('boro level complete ...')

# county/boro
i = 0
tables = []
while i < len(names):
    begin = i
    end = i+50 if i+50 < len(names) else len(names)
    r = json.loads(requests.get(f'https://api.census.gov/data/2010/dec/sf1?get={",".join(names[begin:end])}&for=place:51000&in=state:36&key={api_key}').content)
    df = pd.DataFrame(r[1:])
    df.columns = r[0]
    tables.append(df)
    i += 50

df_city = pd.concat(tables, axis=1, sort=False)
df_city = df_city.loc[:,~df_city.columns.duplicated()]
df_city['geotype'] = 'City2010'
print('city level complete ...')

df_combined = pd.concat([df_tract, df_block, df_boro, df_city], sort=True)
df_combined.to_csv('data/raw.csv', columns=['state', 'place', 'county', 'tract', 'block', 'geotype']+names)
print('output to raw.csv ...')
