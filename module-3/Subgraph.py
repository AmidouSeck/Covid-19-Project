import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from Loader import *

class Subgraph:

    def __init__(self,title,annee,mois,jour):
        self.annee = annee
        self.mois = mois
        self.jour = jour
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self.title = title
        l = Loader()
        cas = l.afficher(f"select nbCas from localites inner join ligne_com_local using(id_localite) inner join communique using(date) where communique.date = '{self.annee}-{self.mois}-{self.jour}' and localites.nom = '{self.title}';")
        if cas == []:
            cas = 0
        else:
            cas = cas[0][0]
        self.addTitle(f"{self.title} : {cas}")
        self.addButton()



    def drawPlot(self, event):
        l = Loader()
        result = l.progressionParRegion(self.title)
        print(result[1])
        self.ax.plot(result[0],result[1])

    def addTitle(self, title):
        self.ax.set_title(title)

    def plot(self):
        x = 1
        plt.show()

    def addButton(self):
        self.axnext = plt.axes([0.71, 0.1, 0.1, 0.075])
        self.bnext = Button(self.axnext, 'Afficher')
        self.bnext.on_clicked(self.drawPlot)
