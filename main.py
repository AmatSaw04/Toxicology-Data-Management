import pandas as pd
from sqlalchemy import create_engine
import urllib
import os
import pyodbc as odbc

server_name = 'Amatya\SQLEXPRESS'
database_name = 'MyDatabase'
driver = 'ODBC Driver 17 for SQL Server'
params = urllib.parse.quote_plus(f"DRIVER={{{driver}}};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes")
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
try:
    conn = odbc.connect(f'DRIVER={driver};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes;')
    print("Connection Successful!")

    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    print(f"Connected to: {row[0]}")
    conn.close()

except Exception as e:
    print(f"Error connecting: {e}")

folder_path = r'C:\Users\AMATYA\Desktop\toxicology data'


def load_file(filename, table_name):
    full_path = os.path.join(folder_path, filename)
    if not os.path.exists(full_path):
        print(f"⚠️ FILE NOT FOUND: {filename}")
        print(f"   Looking in: {folder_path}")
        return

    print(f"📖 Reading: {filename}...")
    try:
        #Changed encoding to 'shift_jis' to handle Japanese characters
        df = pd.read_csv(full_path, sep=',', encoding='shift_jis', on_bad_lines='skip')

        df.columns = df.columns.str.strip()
        print(f"   Columns found: {list(df.columns)[:3]} ")
        print(f"🚀 Loading {len(df)} rows into SQL table: {table_name}")

        # Load to SQL Staging Table
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print("Success!")

    except Exception as e:
        print(f" ERROR loading {filename}:")
        print(f"{e}")


import sqlalchemy as sa

with engine.connect() as conn:
    # Check which server Python is actually touching
    server_check = conn.execute(sa.text("SELECT @@SERVERNAME")).fetchone()[0]
    db_check = conn.execute(sa.text("SELECT DB_NAME()")).fetchone()[0]
    print(f"Python is connected to Server: [{server_check}]")
    print(f"Python is connected to Database: [{db_check}]")

    rows = conn.execute(sa.text("SELECT COUNT(*) FROM Staging_BodyWeights")).fetchone()[0]
    print(f"Rows found in Staging_BodyWeights: {rows}")

    if rows == 0:
        print("PROBLEM: Python says success, but table is empty. Did you forget 'commit'?")
    else:
        print(" SUCCESS: Data is definitely there.")

load_file('open_tggates_main.csv', 'Staging_Compounds')
load_file('open_tggates_individual.csv', 'Staging_Animals')
load_file('open_tggates_biochemistry.csv', 'Staging_Biochemistry')
load_file('open_tggates_body_weight.csv', 'Staging_BodyWeights')
load_file('open_tggates_pathology.csv', 'Staging_Pathology')

print("\n ETL Pipeline Finished.")