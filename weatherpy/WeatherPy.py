from citipy import citipy
import numpy as np
import pandas as pd
import json
import requests
import random
import decimal
import matplotlib.pyplot as plt
import scipy.stats as sp


token = '427a4fb2370419339bc0a94fcb9d8fb8'
url = 'http://api.openweathermap.org/data/2.5/weather?'
num_cities = 2


lat = []
lon = []
temp = []
humidity = []
cloudiness = []
wind_speed = []
cities = []
countries = []
units = 'imperial'

'''
generates lat and lon coordinates to two decimals and adds them to their respective lists
'''
for number in range(num_cities):
    lat.append(round(random.uniform(-90,90),2))
    lon.append(round(random.uniform(-180,180),2))

'''

'''
for number in range(num_cities):
    city = citipy.nearest_city(lat[number],lon[number])
    city_name = city.city_name
    country_code = city.country_code
    print(f'{number+1}. {city_name.upper()}, {country_code.upper()}')
    request_url = url + f'q={city_name},{country_code}&units={units}&appid={token}'
    request = requests.get(request_url).json()
    temp.append(request["main"]["temp"])
    humidity.append(request["main"]['humidity'])
    cloudiness.append(request['clouds']['all'])
    wind_speed.append(request['wind']['speed'])
    cities.append(city_name)
    countries.append(country_code)


weather_dict = {'lat': lat,
                'lon': lon,
                'city': cities,
                'country': countries,
                'temp (f)': temp,
                'humidity (%)': humidity,
                'cloudiness (%)': cloudiness,
                'wind speed (mph)': wind_speed}

weather_df = pd.DataFrame(weather_dict)
north_df = weather_df[weather_df['lat'] >= 0]
south_df = weather_df[weather_df['lat'] < 0]


fig = plt.figure


'''
First subplot comparing temp and latitude
'''
plt.subplot(2,2,1)
plt.scatter(weather_df['lat'],weather_df['temp (f)'])
plt.grid(True)
plt.title('Temp vs. Latitude')
plt.xlabel('Latitude (degrees)')
plt.ylabel('Temperature (F)')
plt.xlim(-90,90)
plt.ylim(-60,100)


'''
Second subplot comparing latitude and humidity
'''
plt.subplot(2,2,2)
plt.scatter(weather_df['lat'],weather_df['humidity (%)'])
plt.grid(True)
plt.title('Humidity vs. Latitude')
plt.xlabel('Latitude (degrees)')
plt.ylabel('Humidity (%)')
plt.xlim(-90,90)
plt.ylim(0,100)


'''
Third subplot comparing latitude and cloudiness
'''
plt.subplot(2,2,3)
plt.scatter(weather_df['lat'],weather_df['cloudiness (%)'])
plt.grid(True)
plt.title('Cloudiness vs. Latitude')
plt.xlabel('Latitude (degrees)')
plt.ylabel('Cloudiness (%)')
plt.xlim(-90,90)
plt.ylim(0,100)


'''
Fourth subplot comparing latitude and wind speed
'''
plt.subplot(2,2,4)
plt.scatter(weather_df['lat'],weather_df['wind speed (mph)'])
plt.grid(True)
plt.title('Wind Speed vs. Latitude')
plt.xlabel('Latitude (degrees)')
plt.ylabel('Wind Speed (mph)')
plt.xlim(-90,90)
plt.ylim(0,100)
plt.show()

weather_df.to_csv('weather_data.csv')







