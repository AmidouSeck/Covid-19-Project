import geopandas as gpd
import matplotlib.pyplot as plt
import os
import pandas as pd
import json
import mysql.connector

localites = {}

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="covid"
)

mycursor = mydb.cursor()
global annee
global mois
global jour
def afficher_sql(annee,mois,jour):
    query = f"select l.* from localite l  inner join communique c  using(id_localite) where c.date = '{annee}/{mois}/{jour}' limit 1;"
    print(query)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    names = mycursor.column_names
    mydict = {}
    j = 1
    while j < len(mycursor.description):
        mydict[f"{names[j]}"] = myresult[0][j]
        j += 1
    return mydict

# def afficher(mois,annee,jour):
#     with open(f'0{mois}-{annee}.json') as json_file:
#         months = json.load(json_file)
#         print(months)
#         for month in months:
#             day = month["date"].split("/")[0]
#             if(int(day) == jour):
#                 l = month["localites"][0]
#                 return l

# req1 = f"select l.annee from localite l  inner join communique ;"

localites = afficher_sql(annee,mois,jour)
print(localites)
map_dict = []
file = os.path.join("senegal_administrative","senegal_administrative.shp")

cities_file = os.path.join("senegal_administrative","sn.csv")

cities = pd.read_csv(cities_file)

# i  = 0
# while i < len(cities.city):
#     map_dict.append(dict(city = cities.city[i],lng = cities.lng[i],lat = cities.lat[i]))
#     i += 1
# print(map_dict)

map = gpd.read_file(file)

axis = map.plot(color='lightblue',figsize = (20,20),linewidth=1,edgecolor = "black")



def_geo = gpd.GeoDataFrame(cities,geometry = gpd.points_from_xy(cities.lng,cities.lat))

i = 0
while i < len(def_geo.city):
    point = def_geo.geometry[i]
    city = def_geo.city[i]
    x = def_geo.lng[i]
    y = def_geo.lat[i]
    cas = localites.get(city)
    print(city)
    if cas is None :
        cas = 0
    axis.annotate(city + " : " + str(cas),xy = (x,y - 0.09))
    i += 1


def_geo.plot(ax = axis,color = "red")



plt.show()

