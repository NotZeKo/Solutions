import requests
import json
import folium

m = folium.Map(location=(55.97885346331034, 10.839257812500002), zoom_start=7)

Api_Key = "api-key=ff0448a3-1ac0-480f-98e8-e77bd0fcf7ad"

test = requests.get("https://api.dataforsyningen.dk/kommuner")
liste = test.json()


def by():
    while True:
        location = input("What city would you like to see? ")
        # Find the matching city
        matching_city = next((city for city in liste if city["navn"].lower() == location.lower()), None)

        # If a match is found, print the bbox and exit the loop
        if matching_city:
            bbox_str = ", ".join(map(str, matching_city['bbox']))
            break
        else:
            print("City not found, try again.")
    city_coords = bbox_str
    return city_coords




def timestamp():
     year = int(input("What year would you like to see?"))
     api_limit = input("What limit would you like to put?")
     url = f"https://dmigw.govcloud.dk/v2/lightningdata/collections/observation/items?bbox={Api_Coordinates}&limit={api_limit}&{Api_Key}&datetime={year}-01-01T00:00:00Z/{year}-12-31T00:00:00Z"
     url = requests.get(url)
     return url

Api_Coordinates = by()
start = timestamp()
thunder_map = json.loads(start.text)


for feature in thunder_map['features']:
    coords = feature['geometry']['coordinates']
    strenght = feature['properties']['amp']
    obs = feature['properties']['observed']
    type_thunder = feature['properties']['type']
    swapped_coords = [coords[1], coords[0]]
    folium.Marker(
        location=swapped_coords,
        tooltip="Info",
        popup=f"Amp: {strenght}<br>Observed: {obs}<br>Type: {type_thunder}",
        icon=folium.Icon(icon="cloud", color="orange",icon_color="#FFFF00"),
    ).add_to(m)
    print(swapped_coords)

m.save("index.html")















