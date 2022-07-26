import logging
from multiprocessing import parent_process
import os
import shutil
import sys
import pandas as pd
import psycopg2

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_connect() -> psycopg2.connect:
    
    conn = None
    params = {
        "port"      : 5432,
        "database"  : "northwind",
        "user"      : "northwind_user",
        "password"  : "thewindisblowing"
    }

    try:
        logging.info('Connecting to PostgreSQL')
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as err:
        logging.info(f'Error: {err}')
        sys.exit(1)
    logging.info('Connected')

    return conn

def get_tables() -> list:
    conn = get_connect()
    cursor = conn.cursor()
    try:
        cursor.execute('''
                SELECT 
                    table_name 
                FROM 
                    information_schema.tables 
                WHERE 
                    table_schema='public'
            ''')
    except (Exception, psycopg2.DatabaseError) as err:
        logging.info(f"Error {err}")
        cursor.close()
        sys.exit(1) 

    all_tables = cursor.fetchall()
    cursor.close()
    
    return list(pd.DataFrame(all_tables)[0].unique())

def get_columns(table: str) -> list:
    
    conn = get_connect()
    cursor = conn.cursor()

    try:
        cursor.execute(f'''
            SELECT
                column_name
            FROM
                information_schema.columns
            WHERE 
                table_name = '{table}'
        ''')
    except (Exception, psycopg2.DatabaseError) as err:
        logging.info(f"Error {err}")
        cursor.close()
        sys.exit(1) 

    all_columns = cursor.fetchall()
    cursor.close()

    return list(pd.DataFrame(all_columns)[0].unique()) 

def convert_postgres_dataframe(table: str) -> pd.DataFrame:
    
    conn = get_connect()
    cursor = conn.cursor()

    columns_name = get_columns(table)
    columns_join = ', '.join(columns_name)
    select_query =  f"SELECT {columns_join} FROM {table}"

    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as err:
        logging.info(f"Error {err}")
        cursor.close()
        sys.exit(1) 
    
    table = cursor.fetchall()
    cursor.close()
 
    return pd.DataFrame(table, columns=columns_name)

def pg_to_csv_by_date(date:str):
    
    tables = get_tables()

    for table in tables:
        path = f"northwind/{table}/{date}/"
        if not os.path.exists(path):
            os.makedirs(path)
        
        df = convert_postgres_dataframe(table)
        
        df.to_csv(path + f"{table}.csv",index=False)
        logging.info(f"{table} csv has been stored.")
        break

    path_csv = f"northwind/order_details/{date}/"
    if not os.path.exists(path_csv):
        os.makedirs(path_csv)
    
    shutil.copy('./data/order_details.csv', path_csv)

    return logging.info("Step 1 done.")
