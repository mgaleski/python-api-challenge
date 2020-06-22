import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import gmaps
import os

api_key = 'AIzaSyAh8w93ad_ufn2nS4hUFOg4bd7XSZyKLqY'
city_df = pd.read_csv('/home/galinux/Python/class/python-api-challenge/output_data/cities.csv')


gmaps.configure(api_key=api_key)

coords = city_df[["Lat", "Lng"]]
humidity = city_df['Humidity']
fig = gmaps.figure()
heat_layer = gmaps.heatmap_layer(coords, weights=humidity, dissipating=False,
                                 max_intensity=300, point_radius=5)

fig.add_layer(heat_layer)


narrowed_city_df = city_df.loc[(city_df["Max Temp"] < 80) & (city_df["Max Temp"] > 70) \
                                    & (city_df["Wind Speed"] < 10) \
                                    & (city_df["Cloudiness"] == 0)].dropna()

hotel_df = narrowed_city_df[["City", "Country", "Lat", "Lng"]].copy()
hotel_df["Hotel Name"] = ""

params = {
    "radius": 5000,
    "types": "lodging",
    "key": api_key
}

for index, row in hotel_df.iterrows():
    lat = row["Lat"]
    lng = row["Lng"]
    params["location"] = f"{lat},{lng}"
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    name_address = requests.get(base_url, params=params)
    name_address = name_address.json()
    try:
        hotel_df.loc[index, "Hotel Name"] = name_address["results"][0]["name"]
    except (KeyError, IndexError):
        print("Missing field/result... skipping.")

info_box_template = """
<dl>
<dt>Name</dt><dd>{Hotel Name}</dd>
<dt>City</dt><dd>{City}</dd>
<dt>Country</dt><dd>{Country}</dd>
</dl>
"""
hotel_info = [info_box_template.format(**row) for index, row in hotel_df.iterrows()]
locations = hotel_df[["Lat", "Lng"]]
marker_layer = gmaps.marker_layer(locations, info_box_content=hotel_info)
fig.add_layer(marker_layer)

