import logging
import os
import sys
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def connect_bigquery():
    try:
        logging.info('Trying to connect...')
        jsonCredentials = './connection/BigQueryCredentials.json'
        credentials = service_account.Credentials.from_service_account_file(
            jsonCredentials,
            scopes = ['https://www.googleapis.com/auth/cloud-platform']
        )

        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        logging.info('Connected to Bigquery')
    
    except Exception as err:
        logging.info(f'Error: {err}')
        sys.exit(1)
    
    return client

def load_bigquery(client: bigquery.Client, table: str, df: pd.DataFrame) -> str:
    try:
        table_id = f"northwind.{table}"
        
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

        job = client.load_table_from_dataframe(
            dataframe=df,
            destination=table_id,
            job_config=job_config
        )

        job.result()

    except Exception as err:
        logging.info(f'Erro {err}')
        sys.exit(1)
    
    logging.info(f'Loaded {df.shape[0]} rows from {table_id}')

def load_data_to_bigquery(date: str):
    conn = connect_bigquery()

    for dirs, subdirs, files in os.walk('northwind'):
        if date in dirs:
            for file in files:
                local_path = os.path.join(dirs, file)
                df_local = pd.read_csv(local_path)
                table = file.replace('.csv','')
                logging.info(load_bigquery(conn,table,df_local))

