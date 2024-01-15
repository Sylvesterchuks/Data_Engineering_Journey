

from aws_credential import *
import mysql.connector
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import text
from mysql.connector import connect, Error
from dotenv import load_dotenv


load_dotenv()

client = boto3.client("rds", region_name=AWS_REGION, verify=False)

DBINSTANCE = os.getenv("DBINSTANCE")

ENDPOINT = os.getenv("ENDPOINT") 
DBNAME = os.getenv("DBNAME") 
AWS_USERNAME = os.getenv("AWS_USERNAME") 
AWS_PASSWORD = os.getenv("AWS_PASSWORD") 
LOCAL_DB_USERNAME = os.getenv("LOCAL_DB_USERNAME") 
LOCAL_DB_PASSWORD = os.getenv("LOCAL_DB_PASSWORD") 

SECURITY_GROUPS = os.getenv("SECURITY_GROUPS") 

# Replace these with your actual values

creds = {
'dbinstance':DBINSTANCE,
'endpoint' : f"{ENDPOINT}.{AWS_REGION}.rds.amazonaws.com", #  Create a rds mysql instance on the AWS webpage and confirm the endpoint format of your rds
'engine' : "mysql",
'engine_version' : "8.0.28",
'dbname' : DBNAME,
'username' : AWS_USERNAME,
'password' : AWS_PASSWORD, #getpass('Enter MySQL Password: '),
'local_db_username' : LOCAL_DB_USERNAME,
'local_db_password' : LOCAL_DB_PASSWORD,
'host':'127.0.0.1',
'port':3306,
'DBInstanceClass':"db.t3.micro",
'AllocatedStorage':20,
'security_groups' : SECURITY_GROUPS #getpass('Enter Security Groups separated by a comma: ').split(',') #e.g: fg-0b870chinume0by
}


def create_rds_database(**kwargs):
    client.create_db_instance(
            DBInstanceIdentifier=kwargs['dbinstance'],
            DBInstanceClass=kwargs['DBInstanceClass'],
            Engine=kwargs['engine'],
            EngineVersion=kwargs['engine_version'],
            DBName=kwargs['dbname'],
            AllocatedStorage=kwargs['AllocatedStorage'],
            MasterUsername=kwargs['username'],
            MasterUserPassword=kwargs['password'],
            Port=kwargs['port'],
            VpcSecurityGroupIds=kwargs['security_groups'],
            DeletionProtection=True
        )
    print("RDS MySQL database created!")


def check_and_create_rds_database(**kwargs):
    client = boto3.client("rds", region_name=AWS_REGION)

    response = client.describe_db_instances()
    if len(response["DBInstances"])!=0:
        for instance in response["DBInstances"]:
            if kwargs['dbinstance'] == instance['DBInstanceIdentifier']:
                print('DB Instance Already Exists')
                break
        else:
            create_rds_database(**kwargs)
    else:
        create_rds_database(**kwargs)

        

        
def create_database(dbname, local_db_username, local_db_password, host, **kwargs):
    try:
        # connect to default database
        conn =  mysql.connector.connect(host=host, user=local_db_username, port='3306', password=local_db_password)
        cur = conn.cursor()
        
        # create servicecalls database with UTF8 encoding
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
        
        # close connection to default databse
        cur.close()
        conn.close()
        
    except Error as e:
        print(e)
    

def create_db(local_machine=True, **kwargs):
    
    if local_machine:
        create_database(**kwargs)        
        
        
    else:
        check_and_create_rds_database(**kwargs)


# Establish a connection to the database
def create_connection(username='admin', password='password', dbname='database', local_machine=True, endpoint='endpoint', **kwargs):
    
    if local_machine==False:
        connection = mysql.connector.connect(
            host=endpoint,
            user=username,
            password=password,
            database=dbname,
            port='3306'
        )
    else:
        connection =  mysql.connector.connect(host=kwargs['host'], database=kwargs['dbname'], user=kwargs['local_db_username'], password=kwargs['local_db_password'], port='3306')
    return connection
