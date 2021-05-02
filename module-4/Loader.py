import mysql.connector
class Loader:
    def afficher(self,query):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        database="corona"
        )
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
        mois = self.afficher("select distinct MONTH(date) from communique order by MONTH(date)")
        donne = self.afficher(f"select sum({region}) {region} from localite l inner join communique c using(id_localite) where YEAR(c.date) = {annee} group by MONTH(c.date)")
        output = []
        outputMois = []
        for x in mois:
            outputMois.append(float(x[0]))
        for x in donne:
            output.append(float(x[0]))
        return [outputMois,output]

p = Loader()
res = p.progressionParRegion("Dakar")
print(res)