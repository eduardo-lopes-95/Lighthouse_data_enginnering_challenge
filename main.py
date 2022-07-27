import logging
import sys
from datetime import datetime
from utils.bigquery import load_data_to_bigquery

from utils.etl_pg import pg_to_csv_by_date
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def main(argv):

    params = sys.argv[1:]
    
    if params:
        if len(params) == 2:
            date = params[1]
            if not validate_date(date):
                logging.info(f'Invalid date. The corret format is format:\nYYYY-MM-DD')
                sys.exit(1)
        else:
            date = datetime.now().strftime("%Y-%m-%d")

    match params:
        case '-e':
            logging.info(pg_to_csv_by_date(date))

        case '-l':
            logging.info(load_data_to_bigquery(date))

        case '-enl':
            logging.info(pg_to_csv_by_date(date))
            logging.info(load_data_to_bigquery(date))

        case _ :
            logging.info("Execution: py main.py <param 1> <param 2>")
            logging.info("1th parameter (mandatory):")
            logging.info("  \n'-e' to run only step 1 \n<-l> to run only step 2 \n<-enl> to run steps 1 and 2")
            logging.info("param 2 (optional): <YYYY-MM-DD>")
            logging.info("If date was not defined, its will consider current date")

def validate_date(date: str) -> bool:
    # using try-except to check for truth value
    res = True
    try:
        res = bool(datetime.parser.isoparse(date))
    except ValueError:
        res = False
    
    return res

if __name__ == "__main__":
   main(sys.argv[1:])