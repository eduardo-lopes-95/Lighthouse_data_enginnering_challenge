import logging
from multiprocessing import parent_process
import sys
import pandas as pd
import psycopg2

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_connect() -> psycopg2.connect:
    
    params = {
        "port"      : 5432,
        "database"  : "northwind",
        "user"      : "postgres",
        "password"  : "admin"
    }

    try:
        logging.info('Connecting to PostgreSQL')
        conn = psycopg2.connect(params)
    except (Exception, psycopg2.DatabaseError) as err:
        logging.info(f'Error: {err}')
        sys.exit(1)
    logging.info('Connected')

    return conn

def list_tables() -> list:

    cursor = get_connect()
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

def list_columns() -> list:

    cursor = get_connect()

    try:
        cursor.execute('''
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
    columns_name = list_columns()
    columns_join = ', '.join()
    select_query =  f"SELECT {columns_join} FROM {table}"

    cursor = get_connect()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as err:
        logging.info(f"Error {err}")
        cursor.close()
        sys.exit(1) 
    
    table = cursor.fetchall()
    cursor.close()
    
    df = pd.DataFrame(table, columns=columns_name)
    return pd.DataFrame(table, columns=columns_name)

def extract_pg():
    
    tables = list_tables()

    for table in tables:
        path = f"northwind_local/{table}/{date}/"
        if not os.path.exists(path):
            os.makedirs(path)
        
        column_names = list_columns(conn,table)
        df = postgresql_to_dataframe(conn, table, column_names)
        
        df.to_csv(path + f"{table}.csv",index=False)
        print(f"{table} csv successfully saved in local disk")

    ## Extract .csv file
    path_csv = f"northwind_local/order_details/{date}/"
    if not os.path.exists(path_csv):
        os.makedirs(path_csv)
    df_csv = pd.read_csv('./data/order_details.csv')
    df_csv.to_csv(path_csv + f"order_details.csv",index=False)

    return f"\nStep 1 done successfully to date: {date} \n"
