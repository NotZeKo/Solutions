import requests
import json
import folium
from prometheus_client import values
m = folium.Map(location=(55.97885346331034, 10.839257812500002), zoom_start=7)



def timestamp():
     year = int(input("What year would you like to see?"))
     url = f"https://dmigw.govcloud.dk/v2/lightningdata/collections/observation/items?bbox=7.888184,54.958694,12.634277,57.803798&limit=2000&api-key=ff0448a3-1ac0-480f-98e8-e77bd0fcf7ad&datetime={year}-01-01T00:00:00Z/{year}-12-31T00:00:00Z"
     url = requests.get(url)
     return url

thunder = timestamp()
thundermap = json.loads(thunder.text)
print(thundermap)
print(type(thundermap))

for feature in thundermap['features']:
    coords = feature['geometry']['coordinates']
    swapped_coords = [coords[1], coords[0]]
    folium.Marker(
        location=swapped_coords,
    ).add_to(m)
    print(swapped_coords)

m.save("index.html")















