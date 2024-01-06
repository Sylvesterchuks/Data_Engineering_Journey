import os
from datetime import timedelta, datetime
import requests
import pandas as pd
import numpy as np
from country import *
from dotenv import load_dotenv


load_dotenv()
WEATHER_API = os.getenv("WEATHER_API") # create an account on https://openweathermap.org/current to get an weather api key

country_name = ''
state_name = ''
return_state=False
return_city=False


def kelvin_to_fahrenheit(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_fahrenheit

def transform_value(data):
    data['temperature_f'] = kelvin_to_fahrenheit(data["temperature_f"])
    data['feels_like_f']= kelvin_to_fahrenheit(data["feels_like_f"])
    data['minimun_temp_f'] = kelvin_to_fahrenheit(data["minimun_temp_f"])
    data['maximum_temp_f'] = kelvin_to_fahrenheit(data["maximum_temp_f"])
    data['time_of_record'] = timestamp_transform(data['time_of_record'])
    data['sunrise_local_time'] = timestamp_transform(data['sunrise_local_time'])
    data['sunset_local_time'] = timestamp_transform(data['sunset_local_time'])
    return data

def timestamp_transform(int_time):
    try:
        return pd.Timestamp.utcfromtimestamp(int_time)
    except:
        return np.nan

def transform_load_data_to_df(task_instance, region=country_name):
    data_list = task_instance
    transformed_data_list = []
    for location, data in data_list.items():
        if data['cod']==200:
                city = data["name"]
                weather_description = data["weather"][0]['description']
                temp_farenheit = data["main"]["temp"]
                feels_like_farenheit= data["main"]["feels_like"]
                min_temp_farenheit = data["main"]["temp_min"]
                max_temp_farenheit = data["main"]["temp_max"]
                pressure = data["main"]["pressure"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                time_of_record = data['dt'] + data['timezone']
                sunrise_time = data['sys']['sunrise'] + data['timezone']
                sunset_time = data['sys']['sunset'] + data['timezone']
        else:
            city = location
            weather_description = ''
            temp_farenheit = None
            feels_like_farenheit= None
            min_temp_farenheit = None
            max_temp_farenheit = None
            pressure = None
            humidity = None
            wind_speed = None
            time_of_record = None
            sunrise_time = None
            sunset_time = None


        transformed_data = {"city": city,
                            "description": weather_description,
                            "temperature_f": temp_farenheit,
                            "feels_like_f": feels_like_farenheit,
                            "minimun_temp_f":min_temp_farenheit,
                            "maximum_temp_f": max_temp_farenheit,
                            "pressure": pressure,
                            "humidty": humidity,
                            "wind_speed": wind_speed,
                            "time_of_record": time_of_record,
                            "sunrise_local_time":sunrise_time,
                            "sunset_local_time": sunset_time                        
                            }
        
        transformed_data_list.append(transformed_data)
    df_data = pd.DataFrame(transformed_data_list)
    df_data = df_data.apply(lambda data: transform_value(data), axis=1)
    cols = df_data.columns[10:]
    df_data[cols] = df_data[cols].apply(pd.to_datetime, errors='coerce')
    

    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    dt_string = f'current_weather_data_{region}_' + dt_string
    df_data.to_csv(f"{dt_string}.csv", index=False)

def get_data_api(url):
    response = requests.request("GET", url)
    data = response.json()
    return data

def extract_data_urls(country_name, 
                 state_name, 
                 return_state, 
                 return_city):
    # print(country_name, state_name, return_state, return_city)
    names = retireve_details(country_name=country_name,
                             state_name=state_name,
                             return_state=return_state,
                             return_city=return_city)
    location_weather_info = {}
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    urls = {location:url.format(location, WEATHER_API) for location in names}
    return urls



