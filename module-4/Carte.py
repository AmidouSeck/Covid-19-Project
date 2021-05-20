import matplotlib.pyplot as plt
import os
import pandas as pd
import json
import mysql.connector
import geopandas as gpd
from matplotlib.widgets import Slider, Button
from Loader import  *

class Carte:
    slidersOn = False

    def annotate(self):
        i = 0
        while i < len(self.def_geo.city):
            point = self.def_geo.geometry[i]
            city = self.def_geo.city[i]
            x = self.def_geo.lng[i]
            y = self.def_geo.lat[i]
            cas = self.mydict.get(city)
            print(city)
            if cas is None:
                cas = 0
            self.an = self.axis.annotate(city + " : " + str(cas), xy=(x, y - 0.09))
            print(self.an)
            i += 1

    def plotMap(self):
        file = os.path.join("senegal_administrative", "senegal_administrative.shp")
        cities_file = os.path.join("senegal_administrative", "sn.csv")
        cities = pd.read_csv(cities_file)
        map = gpd.read_file(file)
        self.axis = map.plot(color='lightblue', figsize=(20, 20), linewidth=1, edgecolor="black")
        self.def_geo = gpd.GeoDataFrame(cities, geometry=gpd.points_from_xy(cities.lng, cities.lat))
        self.def_geo.plot(ax=self.axis, color="red")
    def show(self, annee, mois, jour, sliderEvent=False):
        self.annee = annee
        self.jour = jour
        self.mois = mois
        self.plotMap()
        self.afficher_sql(annee, mois, jour)
        self.annotate()
        plt.show()
    def sourceContamination(self,region,annee,mois,jour):
        region = region.capitalize()
        l = Loader()
        source = l.getClosestRegionWithHighestCases(region,annee,mois,jour)
        coor_region = l.getCoords(region)
        coor_source = l.getCoords(source)
        print(coor_source)
        print(coor_region)
        self.plotMap()
        self.afficher_sql(annee, mois, jour)
        self.annotate()

        # plt.arrow(self.def_geo.lat[0], self.def_geo.lng[0], self.def_geo.lat[2], self.def_geo.lng[2])
        plt.show()


    def afficher_sql(self, annee, mois, jour):
        print(annee, mois, jour)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            database="covid"
        )
        self.mycursor = mydb.cursor()
        query = f"select l.nom,l.nbCas from communique c inner join ligne_com_local  using (date) inner join localites l using(id_localite)  where c.date = '{annee}-{mois}-{jour}'"
        print(query)
        self.mycursor.execute(query)
        myresult = self.mycursor.fetchall()
        self.mydict = {}
        for x in myresult:
            self.mydict[f"{x[0]}"] = x[1]
        print(self.mydict)

