import pandas as pd
from utils.psycopg2_connect import psycopg2_connect
from sqlalchemy import create_engine
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import io
import os

load_dotenv(Path(__file__).parent/'.env')
con = create_engine(os.getenv('EDM_DATA'))
version = os.getenv('VERSION')

df = pd.read_csv('data/final.csv', index_col=False, dtype=str)

db_connection = psycopg2_connect(con.url)
db_cursor = db_connection.cursor()
str_buffer = io.StringIO()

df.to_csv(str_buffer, sep='\t', header=True, index=False)
str_buffer.seek(0)

con.execute(f'CREATE SCHEMA IF NOT EXISTS pff_decennial;')
con.execute(f'''
    DROP TABLE IF EXISTS pff_decennial."{version}";
    CREATE TABLE pff_decennial."{version}" (
        year text,
        geoid text,
        variable text,
        value double precision
    );
''')

db_cursor.copy_expert(f'''COPY pff_decennial."{version}" FROM STDIN WITH NULL AS '' DELIMITER E'\t' CSV HEADER''', str_buffer)
db_cursor.connection.commit()
str_buffer.close()
db_cursor.close()
db_connection.close()

con.execute(f'''
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA pff_decennial to labs;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA pff_decennial_metadata to labs;
    GRANT USAGE ON SCHEMA pff_decennial_metadata TO labs;
    GRANT USAGE ON SCHEMA pff_decennial TO labs;
''')