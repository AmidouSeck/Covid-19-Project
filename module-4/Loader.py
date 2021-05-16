import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

regions = ["Dakar","Thies","Diourbel","Fatick","Kaolack","Kaffrine","Touba","Kolda","Tamba","Ziguinchor","SaintLouis","Matam","Sedhiou","Kedougou","Louga","Tambacounda"]

class Loader:
    def afficher(self,query):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        database="covid"
        )
        print(query)
        self.mycursor = mydb.cursor()
        self.mycursor.execute(query)
        myresult = self.mycursor.fetchall()
        return myresult;
    def progressionGenerale(self,champ):
        mois = self.afficher("select distinct MONTH(date) from communique order by MONTH(date)")
        donne = self.afficher(f"select sum({champ}) from communique group by MONTH(date)")
        output = []
        outputMois = []
        for x in mois:
            outputMois.append(float(x[0]))
        for x in donne:
            output.append(float(x[0]))
        return [outputMois,output]
    def progressionParRegion(self,region,annee = "2020"):
        region = region.capitalize()
        mois = self.afficher(f"select distinct MONTH(c.date) from localites l inner join ligne_com_local lcl using (id_localite) inner join communique c using (date) where l.nom = '{region}' and YEAR(c.date) = '{annee}' group by MONTH(c.date);")
        donne = self.afficher(f"select sum(l.nbCas) from localites l inner join ligne_com_local lcl using (id_localite) inner join communique c using (date) where l.nom = '{region}' and YEAR(c.date) = '{annee}' group by MONTH(c.date);")
        output = []
        outputMois = []
        for x in mois:
            outputMois.append(float(x[0]))
        for x in donne:
            output.append(float(x[0]))
        return [outputMois,output]
    def evolutionCasRegion(self,region,annee = "2020"):
        res = self.progressionParRegion(region,annee)
        mois = res[0]
        x = res[1]
        y = res[1]
        differences = []
        y.append(0)
        i = 0
        while i < len(x) - 1:
            differences.append(abs(x[i] - y[i+1]))
            i = i + 1
        return [mois,differences]
    def getClosestRegion(self,region):
        region = region.capitalize()
        regions = self.afficher(f"select g2.region from geo g,geo g2 where g.region = '{region}' and g.region != g2.region order by st_distance(g.coor,g2.coor)")
        result = []
        for x in regions:
            result.append(str(x[0]))
        return result
    def getClosestRegionWithHighestCases(self,region,annee,mois,jour):
        region = region.capitalize()
        regions = self.afficher(f"select q1.region,q2.nbCas from   (select g2.region,st_distance(g.coor,g2.coor) dist from geo g,geo g2 where g.region = '{region}' and g.region != g2.region order by st_distance(g.coor,g2.coor)) q1 inner join  (select l.nom,l.nbCas from communique c inner join ligne_com_local  using (date) inner join localites l using(id_localite)  where c.date = '{annee}-{mois}-{jour}') q2  on q1.region = q2.nom order by q2.nbCas desc,q1.dist desc limit 1;")
        result = []
        for x in regions:
            result.append(str(x[0]))
        return result[0]
    def getCoords(self,region):
        region = region.capitalize()
        res_x = self.afficher(f"select st_x(coor) + 10 from geo where region = '{region}'")
        res_y = self.afficher(f"select st_y(coor) from geo where region = '{region}'")
        return [res_x[0][0],res_y[0][0]]
    def showMap(self):
        return 0


l = Loader();

region = "Dakar"
x = l.getCoords(region)
y = l.getClosestRegionWithHighestCases(region,2020,5,13)
z = l.getCoords(y)
print(x)
print(y)
print(z)



