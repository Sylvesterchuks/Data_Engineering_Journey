import pandas as pd
import json
import csv
import os
import openpyxl
import logging
from convert_file_utils import *

# reading from countries.json and reading from countries.csv
get_json(output_filename='mycountries.json', csv_filename='countries.csv')
get_csv_file(output_filename='mycountries.csv', json_filename='countries.json')



# Define variable to load the dataframe
dataframe = openpyxl.load_workbook("/content/tmdb.xlsx")

for sheetname in dataframe.sheetnames:
        convert_excel_file(sheetname)



# config our logging to write to an output file
logging.basicConfig(level=logging.DEBUG,
                    filename='log.log',
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    filemode='w',
                    force=True # logging.basicConfig can be run just once, we use "force=True" to reset any previous configuration
                    )

# Notice, while there are five lines of logging, you see only three lines of output if you run this script
logging.debug('Debug message')
logging.info('Info message')
logging.warning('Warning message')
logging.error('Error message')
logging.critical('Critical message')

# reading from and converting a log file to csv
convert_log_file()
