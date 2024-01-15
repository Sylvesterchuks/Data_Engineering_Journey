# Day 31-37: Working with APIs: ETL Automation of Washintgon DC All 311 service request Report Info
![image](https://github.com/Sylvesterchuks/Data_Engineering_Journey/assets/51254935/c015a1b7-18e0-4c00-8990-0d32c16760db)



## Python scripts
List of scripts that will run our ETL automation task in the command line, i.e. Terminal on macOS, and Command Prompt on Windows.

#### Description

**aws_credential.py**

This scripts is used to initialize aws services e.g. client and resources for interacting with aws services.

**get_data.py**

This scripts comprises of functions for downloading and reading the 311 service request file using the API.

**utils.py**

This scripts contains all the functions used for performing different tasks in pipeline. E.g. json_stream or csv_stream for reading json/csv file and uploading to s3 bucket

**s3_utils.py**

This scripts comprises of functions for accessing, uploading and downloading files from s3 bucket.

**tranformation.py**

This scripts contains function used in performing various levels of cleaning and transformation on our dataset.

**create_and_connect_db.py**

This scripts comprises of functions for creating and making conncetions to AWS rds services. Used to create dtabase instance and connect to the database.

**insert_to_db.py**

This scripts comprises of functions for preparing data, creating tables and inserting multiple values into tables.



**run_script.sh**

This is the bash script that runs our washington DC 311 service requests ETL task. It comprises of all the code, functions, modules and scripts for the purpose of extracting, transformation and loading of data to the rds , making it available for dashboarging and ML.

**main.py**

This python script that runs our ETL task like the bash_script above. it is the equivalent of the bash script above with the same workflow.

**cleanup_s3_rds.py**

This scripts comprises of functions to deleting our s3 bucket and rds instance.


##### Installation
<hr>
On your local machine open gitbash and create a folder named weather_etl

    mkdir service_request_etl
Change to the created directory

    cd service_request_etl/
Create a virtual environment

    python -m venv venv
Activate the virtual environment

    source venv/Scripts/activate
    
Clone the git repository

    git clone https://github.com/Sylvesterchuks/Data_Engineering_Journey.git
    
Change to the directory containing our scripts

    cd Data_Engineering_Journey/Day_38_41/
    
Run the `pip install -r requirements.txt` to install all Python packages and their dependencies neede for this task inside the virtual environment.
    
    python -m pip install -r requirements.txt
    
Edit the env file and add your AWS credentials and other basic information, e.g. the databasename, username and password variable in .env file 
```
AWS_DEFAULT_REGION = ''
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

DBINSTANCE = 'dbmysql'
ENDPOINT = "dbmysql.*************" #  Create a rds mysql instance on the AWS webpage and confirm the endpoint format of your rds
DBNAME = "allservicecalls"
AWS_USERNAME = admin	
AWS_PASSWORD = 'admin' #getpass('Enter MySQL Password: ')
LOCAL_DB_USERNAME = 'adminlocalmachine'
LOCAL_DB_PASSWORD = 'adminlocalmachine'

SECURITY_GROUPS = ['sg-*************'] #getpass('Enter Security Groups separated by a comma: ').split(',') 
    
```
    nano .env

Run the below command to get the correct path into scrpaer.bat which can be used in the task scheduler for automation

    sed -i 's\path\'$(pwd)'\g' scraper.bat && sed -i 's\/e\E:\g' scraper.bat


##### To run the script:
- `./run_script.sh` runs the bash file
- `python main.py` runs the python file.
NB: these two are the same script only difference is while one is a bash file, the other is a python file.

![final analysis image](https://github.com/Sylvesterchuks/Data_Engineering_Journey/assets/51254935/35e2e630-12ee-494d-8bd8-9d3f067a33fe)

## General usage information
Download the ZIP package and unzip it.

Most of the scripts will run by simply typing python  followed by the file name of the script, e.g. python Script.py.

If the script is in a different directory from which you are trying to run it, you will need to provide the full path to the script’s file, e.g. python /Users/username/foldername/Script.py.
