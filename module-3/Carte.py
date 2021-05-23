import matplotlib.pyplot as plt
import os
import pandas as pd
import json
import mysql.connector
import geopandas as gpd
from matplotlib.widgets import Slider, Button
from Subgraph import *
import contextily as ctx


class Carte:
    slidersOn = False
    sliderEvent = False
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
        file = os.path.join(os.getcwd(),"module-3","senegal_administrative", "Limite_des_régions.shp")
        cities_file = os.path.join(os.getcwd(),"module-3","senegal_administrative", "sn.csv")
        cities = pd.read_csv(cities_file)
        self.map = gpd.read_file(file)
        # self.map = self.map.to_crs(epsg=3857)
        self.axis = self.map.plot(figsize=(10, 10), alpha=0.05, edgecolor="red")
        self.def_geo = gpd.GeoDataFrame(cities, geometry=gpd.points_from_xy(cities.lng, cities.lat))
        # self.def_geo.plot(ax=self.axis, color="red")
        ctx.add_basemap(self.axis, source="Senegal.tif", alpha=0.6, zorder=8, crs='epsg:4326',zoom=12)
        # ctx.add_basemap(self.axis)
    def addSliders(self):
        axSlider1 = plt.axes([0.1, 0.93, 0.8, 0.02])
        axSlider2 = plt.axes([0.1, 0.95, 0.8, 0.02])
        axSlider3 = plt.axes([0.1, 0.97, 0.8, 0.02])
        self.BarreMois = Slider(axSlider1, "Mois", valmin=1, valmax=12, valfmt="%0.0f",valinit=self.mois)
        self.BarreAnnee = Slider(axSlider2, "Annee", valmin=2019, valmax=2021, valfmt="%0.0f",valinit=self.annee)
        self.BarreJour = Slider(axSlider3, "Jour", valmin=1, valmax=31, valfmt="%0.0f",valinit=self.jour)

        def setMois(val):
            self.mois = int(val)
            self.updateAnnotations(self.annee,self.mois,self.jour)
            self.sliderEvent = True

        def setJour(val):
            self.jour = int(val)
            self.updateAnnotations(self.annee,self.mois,self.jour)
            self.sliderEvent = True

        def setAnnee(val):
            self.annee = int(val)
            self.updateAnnotations(self.annee,self.mois,self.jour)
            self.sliderEvent = True

        self.BarreAnnee.on_changed(setAnnee)
        self.BarreJour.on_changed(setJour)
        self.BarreMois.on_changed(setMois)
        self.slidersOn = True
    def on_click(self,event):
        if self.sliderEvent == True:
            self.sliderEvent = False
            return
        global ix, iy
        ix, iy = event.xdata, event.ydata
        print
        'x = %d, y = %d' % (
            ix, iy)
        global coords
        coords = [iy - 10,ix]
        print(coords)
        iy = iy - 10
        q = f"select  region,  st_distance(coor,ST_GeomFromText('point({iy} {ix})')) as distance  from geo  order by distance limit 1"
        result = self.query(q)
        print(self.annee)
        print(self.mois)
        print(self.jour)
        sb = Subgraph(result[0][0],self.annee,self.mois,self.jour)
        sb.plot()
        return coords
    def show(self, annee, mois, jour, sliderEvent=False):
        self.annee = annee
        self.jour = jour
        self.mois = mois
        self.plotMap()
        self.afficher_sql(annee, mois, jour)
        # self.annotate()
        if self.slidersOn == False:
            self.addSliders()
        if sliderEvent == True:
            plt.draw()
        else:
            plt.connect('button_press_event', self.on_click)
            plt.show()
    def query(self,query):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            database="covid"
        )
        self.mycursor = mydb.cursor()
        self.mycursor.execute(query)
        myresult = self.mycursor.fetchall()
        return myresult
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
