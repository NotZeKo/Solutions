import requests
import pandas as pd
import folium

m = folium.Map(location=(55.97885346331034, 10.839257812500002), zoom_start=7)

url = 'https://query.wikidata.org/sparql'
query = '''SELECT ?railway ?railwayLabel 
       (COALESCE(?officialOpening, ?inception) AS ?openingDate)
       (COALESCE(geof:longitude(?coordinate), geof:longitude(?termCoord)) AS ?longitude)
       (COALESCE(geof:latitude(?coordinate), geof:latitude(?termCoord)) AS ?latitude)
WHERE {
  ?railway wdt:P31 wd:Q728937 ;  # Instance of Railway
           wdt:P17 wd:Q35 .     # Country: Denmark

  OPTIONAL { 
    ?railway wdt:P625 ?coordinate .  # Direct coordinate (if available)
  }
  
  OPTIONAL { 
    ?railway wdt:P559 ?terminus .      # Terminus station(s)
    ?terminus wdt:P625 ?termCoord .     # Coordinate from terminus
  }
  
  OPTIONAL { 
    ?railway wdt:P1619 ?officialOpening .  # Official opening (if available)
  }
  
  OPTIONAL { 
    ?railway wdt:P571 ?inception .  # Inception date (fallback)
  }
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],da,en,sv,de". }
}
ORDER BY ?railwayLabel
'''

r = requests.get(url, params={'format': 'json', 'query': query})
data = r.json()


data_list = []
coords_dic = []

for item in data['results']['bindings']:
    railway_name = item.get('railwayLabel', {}).get('value', 'Unknown')
    opening_year = item.get('openingDate', {}).get('value', 'No opening found')
    longitude = item.get('longitude', {}).get('value', 'No coordinates found')
    latitude = item.get('latitude', {}).get('value', 'No coordinates found')

    data_list.append([railway_name,opening_year , latitude, longitude])
    if longitude != 'No coordinates found' and latitude != 'No coordinates found':
        coords_dic.append({
            "lat": latitude,
            "lon": longitude,
            "name": railway_name,
            "opening": opening_year,
        })



pd.set_option("display.max_rows", None)
df = pd.DataFrame(data_list, columns=["Railway", "Opening Year", "latitude", "longitude"])
df.to_csv('Jernbaner.csv', index=False)



def folium_map ():
    for coord in coords_dic:
        lat = coord['lat']
        lon = coord['lon']
        name = coord['name']
        opening = coord['opening']
        folium.Marker(
            location=[lat, lon],
            tooltip="Info",
            popup=f"Station: {name}<br>Opened: {opening}",
            icon=folium.Icon(icon="cloud", color="orange", icon_color="#FFFF00"),
        ).add_to(m)


folium_map()
m.save("Jernbaner.html")