# Day 31-37: Working with APIs: ETL Automation of World's Daily Weather Data Report Info

## Python scripts
List of scripts that will run our ETL automation task in the command line, i.e. Terminal on macOS, and Command Prompt on Windows.

#### Description

**country.py**

This scripts contains functions that connects to the country state city API using an API key and returns the Countries, States/Provinces and Cities around the world based on the given parameters.

`retrieve_details(country_name, state_name, return_state, return_city) function is used to retrieve countries, states or cities`

**When**

- all parameters are of default value, returns the name and iso_code all countries in the world
- Country_name='China', return_state=True other parameters are of default value, all States/Province in China will be returned.
- Country_name='China', state_name='Shanghai', return_city=True, other parameters are of default value, all cities within a province of China will be returned. 
- Country_name='China' and other parameters are of default value, all cities of China will be returned. 


**weather_etl.py**

Takes charge of all of the weather data urls extraction for every city, state or country using the weather API, transformation function to transform the degrees temperation and datetime formatting and finally loaded ointo a csv file.


**run_script.sh**

This is the bash script that runs our ETL task. It takes some arguments to be passed to the retrieval_details function.
They include:
- -c --country
- -s --state_name
- -rs --return_state
- -rc --return_city

**python_scraper.sh**

This python script that runs our ETL task like the bash_script above. It takes same arguments and follows the the same workflow as the bash script above.


##### Installation
<hr>
On your local machine create a folder and git clone this repository into the created folder. 
change dir to day_31_37
Create and activate a virtual environment


##### Dependencies
<hr>
Run the `pip install -r requirements.txt` to install all Python packages and their dependencies neede for this task inside the virtual environment.


##### To run the script:
- `./run_script.sh` runs the bash file
- `python python_scraper.py` runs the python file.
  
NB: these two are the same script only difference is while one is a bash file, the other is a python file.

## General usage information
Download the ZIP package and unzip it.

Most of the scripts will run by simply typing python  followed by the file name of the script, e.g. python Script.py.

If the script is in a different directory from which you are trying to run it, you will need to provide the full path to the script’s file, e.g. python /Users/username/foldername/Script.py.
