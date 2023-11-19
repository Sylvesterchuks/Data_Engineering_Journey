#!/usr/bin/bash

cd .

source ./venv/Scripts/activate
echo "Currently connected to virtual environment"

python -m pip install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo "Scraping SignalNoise Blog Site and Saving to CSV and JSON"
python signal_post_scraper.py

echo "Saving to SQLite"
python save_to_sqlite.py


username=$1
password=$2
host=$3
database=$4
denormalize=${5:-True}
first_five=${6:-True}

echo "Saving to MySQL"
python save_to_mysql.py -u=$username -p=$password -ho=$host -db=$database -dn=$denormalize -ff=$first_five
