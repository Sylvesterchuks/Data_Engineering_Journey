
from utils import *
from s3_utils import *
from get_data import retrieve_data
from transformation import transform_and_load
from create_and_connect_db import *
from insert_to_db import *



dataset_url = 'https://opendata.arcgis.com/api/v3/datasets/14faf3d4bfbe4ca4a713bf203a985151_0/downloads/data?format=geojson&spatialRefId=4326&where=1%3D1'


# config our logging to write to an output file
logging.basicConfig(level=logging.INFO,
                    # filename='log.log',
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    # filemode='w',
                    handlers=[
                                logging.FileHandler("debug.log"),
                                logging.StreamHandler()
                            ],
                    force=True # logging.basicConfig can be run just once, we use "force=True" to reset any previous configuration
                    )

S3_BUCKET_PREFIX = "service-call-dc-"

BASE_DIR = os.getcwd() #pathlib.Path(__file__).parent.resolve()

S3_BUCKET_NAME, response = create_bucket(S3_BUCKET_PREFIX, s3_client)


buckets = s3_resource.buckets.all()
for mybucket in buckets:
    if S3_BUCKET_NAME == mybucket.name:
        enable_version(mybucket.name)

# list_created_buckets(S3_BUCKET_PREFIX)

service_req_df_json = retrieve_data(dataset_url)

working_buckets = get_working_bucket(S3_BUCKET_PREFIX)

S3_BUCKET_NAME = working_buckets[0].name
data_to_upload = {'All_311_City_Service_Requests_-_Last_30_Days.json' : service_req_df_json} #, 'Roadway_Block.geojson':road_block_df_json}

my_dict = upload_retrieve_data(S3_BUCKET_NAME, 
                     data_to_upload=data_to_upload, 
                     folder_prefix='01_data_collection/01_raw_data_', 
                     format='json', 
                     dtype=False
                     )
service_df = my_dict['All_311_City_Service_Requests_']

# Column Cleaning
service_df.columns = [col.split('.')[-1].lower() if 'geometry' not in col else col.replace('.', '_') for col in service_df.columns]

col_types = {'adddate': 'datetime64[ns]', 'resolutiondate':'datetime64[ns]', 'serviceduedate':'datetime64[ns]',
             'serviceorderdate':'datetime64[ns]', 'inspectionflag':'str', 'inspectiondate':'datetime64[ns]',
             'inspectorname':'str', 'status_code':'str', 'zipcode':'str', 'ward':'str', 'creator':'str',
             'created':'datetime64[ns]', 'editor':'str', 'edited':'datetime64[ns]'}

service_df = service_df.astype(col_types)
dtype_dict = service_df.dtypes.to_dict()


# S3_BUCKET_NAME = working_buckets[0].name
data_to_upload = {'Staging_All_311_City_Service_Requests_-_Last_30_Days.csv': service_df}

my_dict = upload_retrieve_data(S3_BUCKET_NAME, 
                     data_to_upload=data_to_upload, 
                     folder_prefix='first_staging/02_staging_phase_', 
                     format='csv', 
                     dtype=False
                     )
            
staged_service_df = my_dict['Staging_All_311_City_Service_Requests_']
staged_service_df = staged_service_df.astype(dtype_dict)

drop_cols_service_df = staged_service_df.drop(['type', 'inspectionflag', 'inspectiondate', 'inspectorname', 'gis_id', 'globalid', 'creator', 'created', 'editor', 'edited', 'geometry_type'], axis=1)
de_duplicate_service_df = drop_cols_service_df.drop(['geometry_coordinates'], axis=1)

dtype_dict = de_duplicate_service_df.dtypes.to_dict()

# S3_BUCKET_NAME = working_buckets[0].name
data_to_upload = {'Final_Staging_All_311_City_Service_Requests_-_Last_30_Days.csv': de_duplicate_service_df}

my_dict = upload_retrieve_data(S3_BUCKET_NAME, 
                                data_to_upload = data_to_upload, 
                                folder_prefix='final_staging/03_final_staging_phase_', 
                                format='csv', 
                                dtype=False
                                )

final_staging_service_df = my_dict['Final_Staging_All_311_City_Service_Requests_']
final_staging_service_df = final_staging_service_df.astype(dtype_dict)


# S3_BUCKET_NAME = working_buckets[0].name

data_to_upload = transform_and_load(final_staging_service_df, load_csv=True, output_to_local=True)

my_dict = upload_retrieve_data(S3_BUCKET_NAME,  
                     data_to_upload=data_to_upload, 
                     folder_prefix='transformed_data/output', 
                     format='json', 
                     dtype=True
                     )

S3_BUCKET_NAME = working_buckets[0].name
my_dict = download_from_s3(S3_BUCKET_NAME, folder_prefix='transformed_data/output', format='json')

for key in list(my_dict.keys())[::2]:
    my_dict[key] = my_dict[key].astype(my_dict[f'{key}Datatype'].T.to_dict()[0])



# # Connect to the database
# # conn = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:3306/{database}')

# creds = {
# 'dbinstance':DBINSTANCE,
# 'endpoint' : f"{ENDPOINT}.{AWS_REGION}.rds.amazonaws.com", # f"{dbinstance}.***********.{AWS_REGION}.rds.amazonaws.com", #  Create a rds mysql instance on the AWS webpage and confirm the endpoint format of your rds
# 'engine' : "mysql",
# 'engine_version' : "8.0.28",
# 'dbname' : DBINSTANCE,
# 'username' : AWS_USERNAME,
# 'password' : AWS_PASSWORD, #getpass('Enter MySQL Password: '),
# 'local_db_username' : LOCAL_DB_USERNAME,
# 'local_db_password' : LOCAL_DB_PASSWORD,
# 'host':'127.0.0.1',
# 'port':3306,
# 'DBInstanceClass':"db.t3.micro",
# 'AllocatedStorage':20,
# 'security_groups' : SECURITY_GROUPS #getpass('Enter Security Groups separated by a comma: ').split(',') #e.g: fg-0b870chinume0by
# }


dict_df = {key: my_dict[key] for key in list(my_dict.keys())[::2]}
# dict_df = {key: value.fillna(np.nan).replace([np.nan], [None]) for key, value in dict_df.items()} #Change NaN values to None


create_db(local_machine=False, **creds)

save_to_mysql(dict_df, **creds, local_machine=False)
# save_to_mysql(**creds, dict_df, local_machine=False)
# save_to_mysql(**creds, local_machine=False)