# -*- coding: utf-8 -*-
"""

"""
import re
import numpy as np 
import pandas as pd

# load data
df = pd.read_excel("data\\4_Centris_Listing_Plus_Details.xlsx")
print(df.dtypes)

# VARIABLE ZONAGE
#   Au depart, la variable contient une liste de zonage applicable a une propriete. 
#   On doit trouver les valeurs uniques :"categories" dans ces listes puis creer de
#   nouvelles variables indicatrices binaires selon les categories.

# Obtenir la liste des 'categories' de zonage
zonelist = df.Zonage.unique()

zoneall = []
for zone in zonelist:
    for i in zone.split():
        i = i.replace(',', '')
        zoneall.append(i)

x = np.array(zoneall)
zoneunique = np.unique(x)

del i, x, zone, zoneall, zonelist
print(zoneunique)

# creation des variables binaires (get_dummies)
df['Z_Agricole'] = df['Zonage'].str.contains("Agricole")
df['Z_Autre'] = df['Zonage'].str.contains("Autre")
df['Z_Commercial'] = df['Zonage'].str.contains("Commercial")
df['Z_Forestier'] = df['Zonage'].str.contains("Forestier")
df['Z_Industriel'] = df['Zonage'].str.contains("Industriel")
df['Z_Recreotouristique'] = df['Zonage'].str.contains("Récréotouristique")
df['Z_Residentiel'] = df['Zonage'].str.contains("Résidentiel")
df['Z_Villegiature'] = df['Zonage'].str.contains("Villégiature")

df.drop(['Zonage'], axis=1, inplace=True)


# VARIABLE AIRE
#   La variable devrait avoir la meme valeur que la variable Superficie
#   C'est un moyen de valide que les donnees sont correctes. Une erreur signifierait
#   un decalage de ligne entre les 2 datasets (Listing et Details)
df['Aire'] = df['Aire'].str.replace(r'\D+', '')
df['Aire'] = df['Aire'].astype(np.int64)
print("Nombre d'erreurs entre superficie/aire : " + str(len(df) - sum(df['Superficie'] == df['Aire'])))


# VARIABLE POLLDATE
#   Juste besoin de mettre sous format date.
df['Polldate'] = df['Polldate'].astype('datetime64[ns]')


# prendre le code postal dans le champ 'addresse' et mettre dans une col
#   regexp    ^(?!.*[DFIOQU])[A-VXY][0-9][A-Z] ?[0-9][A-Z][0-9]$
#   test:
#       re.search(r'(?!.*[DFIOQU])[A-VXY][0-9][A-Z] ?[0-9][A-Z][0-9]$', df.Adresse[0]).group(0)

df['Adresse'] = df['Adresse'].astype(str)
df['Code_Postal'] = df.Adresse.str.extract(r'((?!.*[DFIOQU])[A-VXY][0-9][A-Z] ?[0-9][A-Z][0-9]$)', expand=False)


# VARIABLE VILLE
#   1. splitter la ville et la sous-categorie(entre parentheses)
#   2. cleaner les espaces
#   3. mettre sous forme de categories

# example:
# 0                  Rouyn-Noranda (Noranda-Nord)
# 1                                Saint-Colomban
# 2                                     La Macaza
# 3          Trois-Rivières (Cap-de-la-Madeleine)
# 4                                  Saint-Damien
#   Pour obtenir Noranda-Nord
    # re.search(r'\((.*?)\)', df.Ville[0]).group(1)
df['Ville_Detail'] = df.Ville.str.extract(r'\((.*?)\)', expand=False)

df['Ville'] = df.Ville.str.replace(r'\((.*?)\)','', regex=True)
df['Ville'] = df.Ville.str.strip()


# VARIABLE GMAP_KEY
# Montreal, QC H1Y 2X7
df['Gmap_key'] = df['Ville'] + ", QC " + df['Code_Postal']
df['Gmap_key'] = df['Gmap_key'].str.strip()
print("Nombre de requetes Google Map API : " + str(len(df.Gmap_key.unique())))
dfgmap = df.Gmap_key.unique()


# prendre les details et creer des variables binaires avec (zonage, bord eau, access eau)
df['Details'] = df['Details'].astype(str)
detailslist = df.Details.unique()

detailsall = []
for detail in detailslist:
    for i in detail.split(", "):
        i = i.replace(',', '')
        detailsall.append(i)

x = np.array(detailsall)
detailunique = np.unique(x)

del i, x, detail, detailsall, detailslist
print(detailunique)


# VARIABLES WATER FRONT, ACCESS
df['Water_front'] = df['Details'].str.contains("Bord")
df['Water_access'] = df['Details'].str.contains("Accès")
df['Water_plan'] = df['Details'].str.contains("Plan")


# faire l'analyse du mot 'rare','magnifique','recherche','beau','superbe','ideal','exceptionnel','reve' dans la description


# Backup to disk
print(df.dtypes)

dfgmap = pd.DataFrame(dfgmap)
dfgmap.to_excel("data\\6_Centris_Gmap.xlsx", index=False)

df.to_excel("data\\5_Centris_Listing_Plus_Details_Clean.xlsx", index=False)
