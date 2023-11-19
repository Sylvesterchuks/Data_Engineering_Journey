
from sqlalchemy import create_engine
import pandas as pd
import sqlite3 as sq
from signal_post_scraper import *

# table and file name
def save_to_sqlite(table_name, file):
    signal_noise = pd.read_csv(f'{file}.csv')
    conn = sq.connect('{}.sqlite'.format(table_name)) # creates file
    signal_noise.to_sql(table_name, conn, if_exists='replace', index=False) # writes to file
    logging.info('Posts loaded to Sqlite')
    conn.close() # good practice: close connection

def read_from_sqlite(table_name):
    conn = sq.connect('{}.sqlite'.format(table_name))
    df = pd.read_sql('select * from {}'.format(table_name), conn)
    conn.close()
    return df

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    # Create arguments
    parser.add_argument('-f', '--file', help="Read file", default='Signal_Blog_posts')
    parser.add_argument('-t', '--tablename', help="Name of Database Table", default='signal_post')
    args = parser.parse_args()
    args = vars(args)

    table_name = args['tablename']
    save_to_sqlite(table_name, file=args['file'])
    read_df = read_from_sqlite(table_name)
