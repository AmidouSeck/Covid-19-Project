import matplotlib.pyplot as plt
import os
import pandas as pd
import json
import mysql.connector
import geopandas as gpd
from matplotlib.widgets import Slider, Button


class Carte:
    slidersOn = False
    an = None
    annotations = []
    def annotate(self):
        if self.an is not None:
            self.an = None
        i = 0
        while i < len(self.def_geo.city):
            point = self.def_geo.geometry[i]
            city = self.def_geo.city[i]
            x = self.def_geo.lng[i]
            y = self.def_geo.lat[i]
            cas = self.mydict.get(city)
            if cas is None:
                cas = 0
            self.an = self.axis.annotate(city + " : " + str(cas), xy=(x, y - 0.09))
            self.annotations.append(self.an)
            i += 1
    def updateAnnotations(self,annee,mois,jour):
        self.afficher_sql(annee,mois,jour)
        print("-----------------------------")
        for a in self.annotations:
            city = a.get_text().split(":")[0].strip()
            new_number = self.mydict.get(city)
            if new_number is None:
                new_number = 0
            new_text = f"{city}:{new_number}"
            a.set_text(new_text)
        print("----------------------------")
        plt.draw()

    def plotMap(self):
        file = os.path.join("senegal_administrative", "senegal_administrative.shp")
        cities_file = os.path.join("senegal_administrative", "sn.csv")
        cities = pd.read_csv(cities_file)
        map = gpd.read_file(file)
        self.axis = map.plot(color='lightblue', figsize=(20, 20), linewidth=1, edgecolor="black")
        self.def_geo = gpd.GeoDataFrame(cities, geometry=gpd.points_from_xy(cities.lng, cities.lat))
        self.def_geo.plot(ax=self.axis, color="red")

    def addSliders(self):
        axSlider1 = plt.axes([0.1, 0.85, 0.8, 0.02])
        axSlider2 = plt.axes([0.1, 0.87, 0.8, 0.02])
        axSlider3 = plt.axes([0.1, 0.89, 0.8, 0.02])
        self.BarreMois = Slider(axSlider1, "Mois", valmin=1, valmax=12, valfmt="%0.0f")
        self.BarreAnnee = Slider(axSlider2, "Annee", valmin=2019, valmax=2021, valfmt="%0.0f")
        self.BarreJour = Slider(axSlider3, "Jour", valmin=1, valmax=31, valfmt="%0.0f")

        def setMois(val):
            self.mois = int(val)
            self.updateAnnotations(self.annee,self.mois,self.jour)

        def setJour(val):
            self.jour = int(val)
            self.updateAnnotations(self.annee,self.mois,self.jour)

        def setAnnee(val):
            self.annee = int(val)
            self.updateAnnotations(self.annee,self.mois,self.jour)

        self.BarreAnnee.on_changed(setAnnee)
        self.BarreJour.on_changed(setJour)
        self.BarreMois.on_changed(setMois)
        self.slidersOn = True

    def show(self, annee, mois, jour, sliderEvent=False):
        self.annee = annee
        self.jour = jour
        self.mois = mois
        self.plotMap()
        self.afficher_sql(annee, mois, jour)
        self.annotate()
        if self.slidersOn == False:
            self.addSliders()
        if sliderEvent == True:
            plt.draw()
        else:
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

c = Carte()
c.show(2020,4,16)
