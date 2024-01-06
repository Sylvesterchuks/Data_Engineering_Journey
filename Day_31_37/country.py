import requests
import os
import json
import pandas as pd
import argparse
from dotenv import load_dotenv


load_dotenv()

headers = {
  'X-CSCAPI-KEY': os.getenv("X_CSCAPI_KEY") # create an account on https://countrystatecity.in/docs/api/all-states/ to get an country, states and cities api key
}

def get_data_api(url, headers):
    response = requests.request("GET", url, headers=headers)
    data = pd.DataFrame(eval(response.text))
    return data


def get_country():
    url = "https://api.countrystatecity.in/v1/countries"
    print('Extracting All Countries Info ...')
    countries = get_data_api(url, headers)
    return countries

def get_state(iso_code, iso_name):
    url = f"https://api.countrystatecity.in/v1/countries/{iso_code}/states"
    print(f'Extracting Info for All Province/States in {iso_name} ...')
    state = get_data_api(url, headers)
    return state

def retireve_details(country_name=None, state_name=None, return_state=False, return_city=False):

    if country_name is None:
        countries = get_country()
        print('Extracting Weather Info for All Countries ...')
        return countries['name'].values

    else:
        countries = get_country()
        
        iso_details = countries.loc[countries['name'].str.lower() == country_name.lower()][['iso2','name']].values[-1]
        iso_code = iso_details[0]
        iso_name = iso_details[-1]

        if return_state:
            state = get_state(iso_code, iso_name)
            print(f'Extracting Weather Info for All Province/States in {iso_name} ...')
            return state['name'].values

        elif state_name and return_city:
            state = get_state(iso_code, iso_name)
            state_code = state.loc[state['name'].str.lower() == state_name.lower()]['iso2'].values[0]
            url = f"https://api.countrystatecity.in/v1/countries/{iso_code}/states/{state_code}/cities"
            cities = get_data_api(url, headers)
            print(f'Extracting Weather Info for All Cities in {state_code}, {iso_name} ...')
            city_names = list({city.replace(' Shi','') for city in cities['name'].values})
            city_names.sort()
            return city_names

        else: 
            url = f"https://api.countrystatecity.in/v1/countries/{iso_code}/cities"
            country_cities = get_data_api(url, headers)
            print(f'Extracting Weather Info for All Cities in {iso_name} ...')
            country_city_names = country_cities['name'].values
            return country_city_names
    