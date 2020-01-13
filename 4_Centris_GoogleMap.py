excel# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 10:48:04 2020

@author: captn
"""

import pandas as pd
import pickle
import googlemaps
from datetime import datetime

now = datetime.now()
df = pd.read_excel("data\\6_Centris_Gmap.xlsx")

# instanciate a client
API_key = "yourkey"
gmaps = googlemaps.Client(key=API_key)

home = "Montreal, QC H1Y 2X7"

# CONTROL SWITCH (dont wan't to pay for API)
# Can skip one or the other API call
ok = False

## 
## DATA FROM DISTANCE_MATRIX API
## 

# notes:
#
#   Saguenay, QC G7K 0B4   <<<<< n'existe pas
#   'rows': [{'elements': [{'status': 'NOT_FOUND'}]}]

# test:
#   dist_result = gmaps.distance_matrix(home, 'Saint-Faustin/Lac-Carré, QC J0T 1J2', mode='driving')
#   dist_error = gmaps.distance_matrix(home, 'Saguenay, QC G7K 0B4', mode='driving')

if ok is True:
    dist_list = []
    for ind, land in df.iterrows():
        print(land[0])
        
        dist_result = gmaps.distance_matrix(home, land, mode='driving')
        print(dist_result)
    
        if (dist_result['rows'][0]['elements'][0]['status'] == 'NOT_FOUND'):
            dist_list.append([land[0], None, None])
        else:
            dist_list.append([land[0], dist_result['rows'][0]['elements'][0]['distance']['value'], dist_result['rows'][0]['elements'][0]['duration']['value']])
        
    df2 = pd.DataFrame(dist_list, columns=['destination','Distance','Duration'])
    df2.to_excel("data\\7_Gmap_distance_matrix.xlsx", index=False)

## 
## DATA FROM GEO_LOCALISATION API
## 

if ok is True:
    # get data from gmap geoloc API and save to pickle
    # i want to do it only once
    geo_jsons = {}
    for ind, land in df.iterrows():
        print(land[0])
        geo_result = gmaps.geocode(land[0])
    
        geo_jsons[land[0]] = geo_result
    
    f = open("data\\Gmap_geoloc_json_dict.pkl","wb")
    pickle.dump(geo_jsons,f)
    f.close()
    
# Now process the geo_jsons dictionnary
# it contains all answers(json) by gmap API with the key being the adress requested
# so the key may be used to join the data to Centris.

# reload the pickle if needed
file = open('data\\Gmap_geoloc_json_dict.pkl', 'rb')
geo_jsons = pickle.load(file)
file.close()

geo_list = []

for key in geo_jsons.keys():
    print(key)

    if len(geo_jsons[key]) == 0:
        output = {
            "formatted_address" : None,
            "latitude": None,
            "longitude": None,
            "coord_type": None,
            "gmap_id": None,
            "gmap_type": None,
            "postcode": None,
            "quartier": None,
            "ville": None,
            "region": None,
            "province": None,
            "pays": None
        }
    else:    
        answer = geo_jsons[key][0]
        output = {
            "formatted_address" : answer.get('formatted_address'),
            "latitude": answer.get('geometry').get('location').get('lat'),
            "longitude": answer.get('geometry').get('location').get('lng'),
            "coord_type": answer.get('geometry').get('location_type'),
            "gmap_id": answer.get("place_id"),
            "gmap_type": ",".join(answer.get('types')),
            "postcode": ",".join([x['long_name'] for x in answer.get('address_components') 
                                  if 'postal_code' in x.get('types')]),
            "quartier": ",".join([x['long_name'] for x in answer.get('address_components') 
                      if 'administrative_area_level_3' in x.get('types')]),
            "ville": ",".join([x['long_name'] for x in answer.get('address_components') 
                      if 'locality' in x.get('types')]),
            "region": ",".join([x['long_name'] for x in answer.get('address_components') 
                      if 'administrative_area_level_2' in x.get('types')]),
            "province": ",".join([x['long_name'] for x in answer.get('address_components') 
                      if 'administrative_area_level_1' in x.get('types')]),
            "pays": ",".join([x['long_name'] for x in answer.get('address_components') 
                      if 'country' in x.get('types')])
        }

    geo_list.append([key, output])

# backup
f = open("data\\Gmap_geoloc_2_key_dict.pkl","wb")
pickle.dump(geo_list,f)
f.close()

todf = []
for i, j in geo_list:
    todf.append([i,
    j["formatted_address"],
    j["latitude"],
    j["longitude"],
    j["coord_type"],
    j["gmap_id"],
    j["gmap_type"],
    j["postcode"],
    j["quartier"],
    j["ville"],
    j["region"],
    j["province"],
    j["pays"]])

dffinal = pd.DataFrame(todf, columns=["key","formatted_address","latitude","longitude","coord_type","gmap_id","gmap_type","postcode","quartier","ville","region","province","pays"])
dffinal.to_excel("data\\Gmap_geoloc_final.xlsx", index=False)