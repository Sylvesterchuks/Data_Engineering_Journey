from create_and_connect_db import *
from utils import *

def create_tables(conn, df_dict, local_machine):
    str_dt = 'VARCHAR'
    texttype = 'TEXT'
    int_dt = 'INTEGER'
    dec = 'DECIMAL'
    bool_ = 'BOOL'
    date_dt = 'TIMESTAMP'
    
    create_serviceFacts_table_query = f"""
                CREATE TABLE serviceFacts(
                    servicerequestid {str_dt}(25) NOT NULL PRIMARY KEY,
                    servicecode {str_dt}(50),
                    status_id {int_dt},
                    address_id {int_dt},
                    adddate {date_dt},
                    resolutiondate {date_dt},
                    serviceduedate {date_dt},
                    serviceorderdate {date_dt},
                    details {texttype},
                    servicecallcount {int_dt}
                )
                """
    create_dimLocation_table_query = f"""CREATE TABLE dimLocation (
                                        address_id {int_dt} NOT NULL PRIMARY KEY,
                                        streetaddress {str_dt}(100),
                                        xcoord {dec},
                                        ycoord {dec},
                                        latitude {dec}(12,7),
                                        longitude {dec}(12,7),
                                        city {str_dt}(25),
                                        state {str_dt}(25),
                                        zipcode {str_dt}(20),
                                        maraddressrepositoryid {int_dt},
                                        ward {str_dt}(10)
                                        )
                                        """

    create_dimDate_table_query = f"""CREATE TABLE dimDate (
                                        Date {date_dt} NOT NULL PRIMARY KEY,
                                        year {int_dt},
                                        months {int_dt},
                                        day {int_dt},
                                        week {int_dt},
                                        dayofweek {int_dt},
                                        quarter {int_dt},
                                        is_weekend {bool_},
                                        hour {int_dt},
                                        time_of_day {str_dt}(20)
                                        )
                                        """


    create_dimServiceType_table_query = f"""CREATE TABLE dimServiceType (
                                        servicecode {str_dt}(20) NOT NULL PRIMARY KEY,
                                        servicecodedescription {str_dt}(255),
                                        servicetypecodedescription {str_dt}(255),
                                        organizationacronym {str_dt}(50)
                                        )
                                        """
    create_dimServiceStatus_table_query = f"""CREATE TABLE dimServiceStatus (
                                    status_id {int_dt} NOT NULL PRIMARY KEY,
                                    priority {str_dt}(20),
                                    serviceorderstatus {str_dt}(25),
                                    status_code {str_dt}(10)
                                    )
                                    """
    tables = {key.split('.')[0] : [",".join([str(i) for i in values.columns.tolist()]), values] for key, values in df_dict.items()}
    


    if local_machine:
        with conn.connect() as connection:
            for key, values in df_dict.items():
                tblname = key.split('.')[0]
                insert_value = [",".join([str(i) for i in values.columns.tolist()]), values]
                print(insert_value[1].shape)
                print(f"DROP Table IF EXISTS {tblname}")
                connection.execute(text(f"DROP Table IF EXISTS {tblname}"))
                connection.execute(text(eval(f"create_{tblname}_table_query")))
                print(f'{tblname} created successfully')
                logging.info(f"{tblname} with a defined datatype and constraint created successfully")

                insert_into_table(table_name=tblname, df=insert_value[1], cols=insert_value[0], connection=connection)
    else:
        with conn as connection:
            cursor = connection.cursor()
            for key, values in df_dict.items():
                tblname = key.split('.')[0]
                insert_value = [",".join([str(i) for i in values.columns.tolist()]), values]
                print(insert_value[1].shape)
                cursor.execute(f"DROP Table IF EXISTS {tblname}")
                cursor.execute(eval(f"create_{tblname}_table_query"))
                print(f'{tblname} created successfully')
                logging.info(f"{tblname} with a defined datatype and constraint created successfully")

                insert_into_table(table_name=tblname, df=insert_value[1], cols=insert_value[0], connection=cursor, local_machine=False)
                connection.commit()
        print('All Tables Created and Data Inserted Successfully')


def get_indices(x: list, value: int) -> list:
    """
    This function gets the index values of any given value from x list
    """
    indices = list()
    i = 0
    while True:
        try:
            # find an occurrence of value and update i to that index
            i = x.index(value, i)
            # add i to the list
            indices.append(i)
            # advance i by 1
            i += 1
        except ValueError as e:
            break
    return indices


def remove_null_col_value(cols, row):
    """
    This function iterates through columns and rows, then removes the index value where in both column and rows where row value is None
    """
    table_col = cols.split(',')
    idxs = get_indices(list(row), None)
    trow = list(row)
    for idx, j in enumerate(idxs):
        table_col.pop(j-idx)
        trow.pop(j-idx)
    row = trow
    table_col = ','.join(table_col)
    return table_col, row


# def insert_into_table(table_name, df, cols, connection, local_machine=True):
#     logging.info(f'Inserting Records into {table_name} table')
   
#     # Insert DataFrame recrds one by one.
#     for i, row in df.iterrows():
#         table_col = cols
#         if None in tuple(row):
#             table_col, row = remove_null_col_value(cols, row)
#         sql = f"INSERT INTO {table_name} ({table_col}) VALUES {tuple(row)}"
#         if local_machine:
#             connection.execute(text(sql))
#         else:
#             connection.execute(sql)
#     logging.info(f'{i+1} Records successfully Inserted into {table_name} table')
#     print(f'{i+1} Records successfully Inserted')



def insert_into_table(table_name, df, cols, connection, local_machine=True):
    logging.info(f'Inserting Records into {table_name} table')
    df = df.where((pd.notnull(df)), None)
    
    sql = f"""INSERT INTO {table_name} ({cols}) VALUES ({'%s, '* (len(cols.split(','))-1)}%s)"""
    
    if local_machine:
        connection.executemany(text(sql),df.values.tolist())
    else:
        connection.executemany(sql, df.values.tolist())
    logging.info(f'{df.shape[0]} Records successfully Inserted into {table_name} table')
    print(f'{df.shape[0]} Records successfully Inserted')


def save_to_mysql(df_dict, local_machine=False, **kwargs):
    
    if local_machine==False:
        conn = create_connection(local_machine=False, **kwargs)
        # cursor = connection.cursor()

    else:
        # Connect to the database
        conn = create_engine(f'mysql+mysqlconnector://{kwargs["local_db_username"]}:{kwargs["local_db_password"]}@{kwargs["host"]}:3306/{kwargs["dbname"]}')
    logging.info('Connected to mySQL Engine')

    print('Creating Tables...')
    create_tables(conn, df_dict, local_machine)
    # create_tables(conn, local_machine)




# Select records
def select_records(connection, tablename):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {tablename} LIMIT 5")
    rows = cursor.fetchall()
    print(rows)
    for row in rows:
        print(row)

# save_to_mysql(**creds, df_dict, local_machine=False)
# save_to_mysql(username, password, host, dbname)
