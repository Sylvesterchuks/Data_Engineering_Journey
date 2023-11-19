
from sqlalchemy import create_engine
from sqlalchemy import text
from signal_post_scraper import *
# from mysql.connector import connect, Error

def denormalize_dataframe(file, conn, denormalize=True):
    
    read_df = pd.read_csv(file)
    
    # with conn.connect() as connection:
        # connection.execute(text("DROP TABLE posts_denormalized"))

    
    if denormalize==True:
        # Write the DataFrame to the database
        
        read_df.to_sql(name='posts_denormalized', con=conn, if_exists='replace', index=False)
        logging.info('Write dataframe to database using pandas to_sql')
        return read_df, None

    else:
        # Creating authors table and removing duplicate values
        authors = read_df['author'].drop_duplicates().reset_index().reset_index()
        authors['level_0'] = authors['level_0'].apply(lambda x: x + 1 )
        authors.rename(columns={'level_0':'author_id', 'author':'author_name'}, inplace=True)
        authors.drop(['index'], axis=1, inplace=True)


        # Adding author-id key by merging author table to post table
        posts_authors_df = read_df.merge(authors, left_on='author', right_on='author_name')
        posts_authors_df.drop(['author_name', 'author'], axis=1, inplace=True)
        posts_authors_df = posts_authors_df.reset_index().reset_index()
        posts_authors_df['level_0'] = posts_authors_df['level_0'].apply(lambda x: x + 1 )
        posts_authors_df.rename(columns={'level_0':'post_id'}, inplace=True)
        posts_authors_df.drop(['index'], axis=1, inplace=True)
        return posts_authors_df, authors


def create_tables(conn):
    create_posts_table_query = """
                    CREATE TABLE posts_info(
                        post_id INT AUTO_INCREMENT PRIMARY KEY,
                        date_posted DATE,
                        title VARCHAR(255),
                        description TEXT,
                        number_of_comments INT,
                        post_link VARCHAR(255),
                        author_id INT
                    )
                    """
    create_authors_table_query = """CREATE TABLE authors_table (
                                            author_id INT AUTO_INCREMENT PRIMARY KEY,
                                            author_name VARCHAR(45))
                                            """


    with conn.connect() as connection:
        connection.execute(text("DROP TABLE IF EXISTS posts_info"))
        connection.execute(text("DROP TABLE IF EXISTS authors_table"))
        connection.execute(text(create_authors_table_query))
        logging.info('authors_table with a defined datatype and constraint created successfully')
        connection.execute(text(create_posts_table_query))
        logging.info('posts_info with a defined datatype and constraint created successfully')
        print('Tables Created')

def insert_into_table(table_name, df, cols, conn):
    logging.info(f'Inserting Records into {table_name} table')
    with conn.connect() as connection:
        # Insert DataFrame recrds one by one.
        for i, row in df.iterrows():
            sql = f"INSERT INTO {table_name} ({cols}) VALUES {tuple(row)}"
            connection.execute(text(sql))
        logging.info(f'{i+1} Records successfully Inserted into {table_name} table')
        print(f'{i+1} Records successfully Inserted')



def save_to_mysql(username, password, host, database, file, denormalize=True, first_five=False):
    
    # Connect to the database
    conn = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:3306/{database}')
    logging.info('Connected to mySQL Engine')

    posts_authors_df, authors = denormalize_dataframe(file=file, conn=conn, denormalize=denormalize)

    
    # Retrieve the table using pandas function
    if first_five==True:
        read_df = pd.read_sql('select * from posts_denormalized', conn)
        print(read_df.head())
    # print(denormalize==False)
    
    if denormalize==False:
        print('Creating Tables...')
        create_tables(conn)
        # creating author columns list for insertion
        author_cols = ",".join([str(i) for i in authors.columns.tolist()])
        # creating post_info columns list for insertion
        post_cols = ",".join([str(i) for i in posts_authors_df.columns.tolist()])
        tables = {'posts_info': [post_cols, posts_authors_df], 'authors_table': [author_cols, authors]}
        
        for key,values in tables.items():
            insert_into_table(table_name=key, df=values[1], cols=values[0], conn=conn)

if __name__=="__main__": 

    import argparse
    parser = argparse.ArgumentParser()

    #database = "connectdatabase"
    #os.environ['DB_HOST'] = host # input('Enter MySQL Host Name: ')
    #os.environ['DB_USERNAME'] = username # input('Enter MySQL Database  Username: ')
    #os.environ['DB_PASSWORD'] = password #  input('Enter MySQL Database Password: ')

    # Create another group for authentication
    auth_group = parser.add_argument_group('Authentication', 'Login credentials')

    auth_group.add_argument("-u", "--username", help="Username to connect to a database server")
    auth_group.add_argument("-p", "--password", help="Password to connect to a database server")
    auth_group.add_argument("-ho", "--host", help="Database server host")
    auth_group.add_argument("-db", "--database", help="Database name to be connected to")
    parser.add_argument('-f', '--file', help="Normalize Database", default='Signal_Blog_posts.csv')
    parser.add_argument('-dn', '--denormalize', type=lambda s: s.lower() in ['true', 't', 'yes', '1'], help="Normalize Database", default=True)
    parser.add_argument('-ff', '--first_five', type=lambda s: s.lower() in ['true', 't', 'yes', '1'], help="Prints first five records.", default=False)

    args = parser.parse_args()

    args = vars(args)
    save_to_mysql(args['username'], args['password'], args['host'], args['database'], file=args['file'], denormalize=args['denormalize'], first_five=args['first_five'])
