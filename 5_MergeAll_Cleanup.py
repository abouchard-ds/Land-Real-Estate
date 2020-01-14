# -*- coding: utf-8 -*-
"""

"""
import pandas as pd

df1 = pd.read_excel("data\\5_Centris_Listing_Plus_Details_Clean.xlsx")
df2 = pd.read_excel("data\\Gmap_geoloc_final.xlsx")
df3 = pd.read_excel("data\\7_Gmap_distance_matrix.xlsx")

# les deux datasets de GMAP sont issue de la meme liste dans le meme ordre
# il suffit de valider qu'ils ont bien 2616 chaque et les premieres ligne sont identiques
df4 = pd.concat([df2, df3], axis=1)


# col 0 et 13 devraient matcher
print("Nombre de mismatch entre les datasets de Google Map 'Distance Matrix' et 'Geolocalisation' = " + str(len(df4)-sum(df4['key'] == df4['destination'])))

# Maintenant on peut joindre les df4 et df1 sur df4[0] et df1['Gmap_key']
dffinal = pd.merge(df1, df4, left_on='Gmap_key', right_on='key', how='left')

dffinal.to_excel("data\\Centris_Final_Dataset.xlsx", index=False)

### CLEANUP
del df1,df2,df3,df4

# remove temporary or duplicated variables
dffinal.drop(['Aire', 'Details', 'Gmap_key', 'postcode', 'key', 'province', 'pays', ], axis=1, inplace=True)

print(list(dffinal.columns.values))

print(dffinal.dtypes)

dffinal['Distance_KM'] = (dffinal['Distance'] / 1000)
dffinal['Duration_H'] = (dffinal['Duration'] / 3600)

# remove prices under 1000 (8947 passe a 8717)
dffinal = dffinal[dffinal.Prix >= 1000]

dffinal.Ville.unique()
len(dffinal.Ville.unique())

dffinal.to_excel("data\\Centris_Final_Dataset_Clean.xlsx", index=False)

# drop from 8717 to 3988
alex = dffinal[(dffinal.Duration_H <= 2.1) & (dffinal.Prix_PC <= 5)]
alex.to_excel("First_Selection_2.xlsx", index=False)

# # graph 
# # get image from openmaps
BBox = ((alex.longitude.min(), alex.latitude.min(), alex.longitude.max(), alex.latitude.max()) )

import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon

geometry = [Point(xy) for xy in zip(alex['longitude'], alex['latitude'])]
geometry[:3]

crs = {'init':'epsg:4326'}
geo_df = gpd.GeoDataFrame(alex, crs = crs, geometry = geometry)
geo_df.head()

qc_map = gpd.read_file('map\\terrains_quebec_planet_osm_line_lines.shp')
fig,ax = plt.subplots(figsize = (30,30))
qc_map.plot(ax = ax, alpha = 0.4, color ="grey")

geo_df.plot(ax=ax,markersize=20,color="blue",marker="o",label="Terrains")
plt.legend(prop={'size':15})
plt.savefig('filename.png', dpi=300)
