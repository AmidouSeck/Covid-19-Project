from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog,simpledialog
from PIL import ImageTk, Image
import os
import pymysql
import json
import glob


home=Tk()
# Configuration de la page d'acceuil
# home.configure(bg="blue")
#Constants
home.update()
widthOfScreen = home.winfo_screenwidth()
heightOfScreen = home.winfo_screenheight()
widthOfWindow = home.winfo_screenwidth()
heightOfWindow = home.winfo_screenheight()

x_coordinate = (widthOfScreen/2)-(widthOfWindow/2)
y_coordinate = (heightOfScreen/2)-(heightOfWindow/2)
home.title('COVID 19 MODELER')
home.geometry("%dx%d+%d+%d"%(widthOfWindow,heightOfWindow,x_coordinate,y_coordinate))

my_image = ImageTk.PhotoImage(Image.open('image\\homePage.jpg'))
image_label= Label(image=my_image, width= widthOfWindow, height=heightOfWindow)
image_label.pack()


#global variable
global chBList
chBList = []
dateCom = []
chbudraw = False
savePoint = "P1"
user_id = StringVar()
user_password = StringVar()
con =  pymysql.connect(host="localhost", user="root", password="", database="covid", connect_timeout=28800)
cur = con.cursor()
# con.query('SET GLOBAL connect_timeout=28800')
# con.query('SET GLOBAL interactive_timeout=28800')
# con.query('SET GLOBAL wait_timeout=28800')

#Functions
def checkboxDraw(days):
    chbudraw = True
    days.sort()
    global chBvar
    chBvar = []
    for i in range(len(days)):
        chBvar.append(IntVar())

    left = 60
    right = 60
    i=0
    if len(chBList) > 0:
        for chB in chBList:
            chB.destroy()
    chBList.clear()
    for day in days:
        chBList.append(Checkbutton(frameLoaderRight, text=day, bg="#28527a", fg="black", variable=chBvar[i], command= chBListener))
        i+=1

    for i in range(len(chBList)):
        if i < 15:
            chBList[i].place(x=200, y=left)
            left += 30
        else:
            chBList[i].place(x=400, y=right)
            right += 30
    # Affichage des buttons SelectAll et DeselectAll
    buttonSelectAll.configure(state=NORMAL)
    buttonDeselect.configure(state=NORMAL)

#function getSize()
def getWidth(p):
    return widthOfScreen*(p/100)

def getHeight(p):
    return heightOfScreen*(p/100)


def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("JSON files",
															"*.json"),
														("XML files",
															"*.xml")))

    # Change label contents
    labfilename.configure(text="File Opened: " + filename)
    if filename != None:
        openFile(filename)

def openFile(filename):
    global data
    with open(filename) as jsonFile:
        data = json.load(jsonFile)
        global days
        days = []
        for i in data:
            date = i["date"]
            days.append(date[:2])
        # if chbudraw == True:
        #     destroyChButton()
        checkboxDraw(days)

def destroyChButton():
    print(len(chBList))
    if len(chBList) > 0:
        for chB in chBList:
            chB.destroy()

#AUTH FOR DATA EXPLORER FRAME

def DrawExploreAuthFrame():
    global user_id
    global user_password
    global exploreFrame
    exploreFrame = Frame(home, width=300, height=130, bg="#8ac4d0", bd=6, relief="ridge")
    exploreFrame.grid_propagate(0)
    exploreFrame.update()
    frameLoaderRight.update()
    home.update()
    exploreFrame.place(x=widthOfWindow/2-150, y=heightOfWindow/2-65)
    labId = Label(exploreFrame, text="Identifiant", bg="#8ac4d0")
    labPassword = Label(exploreFrame, text="Password", bg="#8ac4d0")
    entId = Entry(exploreFrame, width=30 , textvariable = user_id)
    entId.focus_set()
    entPass = Entry(exploreFrame, width= 30, textvariable = user_password, show="*")
    buttonOK = Button(exploreFrame, text=" OK ", command= logExplore)
    buttonAbort = Button(exploreFrame, text=" Cancel ", command=exploreFrame.destroy)
    labId.grid(row=0, column=0, pady=10, padx=15)
    entId.grid(row=0, column=1)
    labPassword.grid(row=1, column=0)
    entPass.grid(row=1, column=1)
    exploreFrame.update()
    buttonOK.update()
    buttonOK.place(x=exploreFrame.winfo_width()/3, y= exploreFrame.winfo_height()*0.7)
    buttonAbort.place(x=exploreFrame.winfo_width() / 2 - buttonOK.winfo_width(), y=exploreFrame.winfo_height() * 0.7)

# explore function
def explore():
    exploreFrame.destroy()
    os.system('python explore.py')

#exlpore auth
def logExplore():
    if user_id.get() == "" or user_password.get() == "":
        messagebox.showerror("Erreur", "Veillez entrer un ID et un mot de passe", parent=frameLoaderRight)
    else :

        try:
            global  con
            global  cur
            con = pymysql.connect(host="localhost", user="root", password="", database="mysql")
            cur = con.cursor()
            cur.execute("select user from user where user='"+user_id.get()+"' and authentication_string= CONCAT('*',UPPER(SHA1(UNHEX(SHA1('"+user_password.get()+"')))))")
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("Erreur", "Identifiant ou mot de passe invalide", parent=home)

            else:
                messagebox.showinfo("Réussi", "Vous pouvez explorer les données", parent=home)
                exploreFrame.destroy()
            waithere()

            # loader()
            con.close()
            explore()
        except Exception as es:
            messagebox.showerror("Erreur", f"Erreur due a : {str(es)}", parent=home)

def waithere():
    var = IntVar()
    home.after(3000, var.set, 1)
    print("waiting...")
    home.wait_variable(var)

def DrawImportAuthFrame():
    global user_id
    global user_password
    global importFrame
    global chbutton
    chbutton= IntVar()
    importFrame = Frame(home, width=300, height=130, bg="#8ac4d0", bd=6, relief="ridge")
    importFrame.grid_propagate(0)
    importFrame.update()
    frameLoaderRight.update()
    home.update()
    importFrame.place(x=widthOfWindow/2-150, y=heightOfWindow/2-65)
    labId = Label(importFrame, text="Identifiant", bg="#8ac4d0")
    labPassword = Label(importFrame, text="Password", bg="#8ac4d0")
    entId = Entry(importFrame, width=30 , textvariable = user_id)
    entId.focus_set()
    entPass = Entry(importFrame, width= 30, textvariable = user_password, show="*")
    transactionMode = Checkbutton(importFrame, text="Mode transactionel", pady=5, bg="#8ac4d0", variable= chbutton)
    buttonOK = Button(importFrame, text="   OK   ", command= load)
    buttonAbort = Button(importFrame, text="   Cancel   ", command=importFrame.destroy)
    labId.grid(row=0, column=0, pady=10, padx=15)
    entId.grid(row=0, column=1)
    labPassword.grid(row=1, column=0)
    entPass.grid(row=1, column=1)
    importFrame.update()
    transactionMode.grid(row=2, columnspan=2)
    buttonOK.update()
    buttonOK.place(x=importFrame.winfo_width()/3, y= importFrame.winfo_height()*0.7)
    buttonAbort.place(x=importFrame.winfo_width()/2-buttonOK.winfo_width(), y= importFrame.winfo_height()*0.7)
def load():
    if user_id.get() == "" or user_password.get() == "":
        messagebox.showerror("Erreur", "Veillez entrer un ID et un mot de passe", parent=frameLoaderRight)
    else :

        try:
            global  con
            global  cur
            con = pymysql.connect(host="localhost", user="root", password="", database="mysql")
            cur = con.cursor()
            cur.execute("select user from user where user='"+user_id.get()+"' and authentication_string= CONCAT('*',UPPER(SHA1(UNHEX(SHA1('"+user_password.get()+"')))))")
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("Erreur", "Identifiant ou mot de passe invalide", parent=home)

            else:
                messagebox.showinfo("Success", "Vous etes connecté", parent=home)
                con = pymysql.connect(host="localhost", user="root", password="", database="covid", port=3308, connect_timeout=28800)
                cur = con.cursor()
                importFrame.destroy()
                selectedChButtonList = []
                i = 0
                for chbutton, var in zip(chBList, chBvar):
                    if var.get()==1:
                        # the checkbutton is selected
                        selectedChButtonList.append(chbutton.cget("text"))
                extractData(selectedChButtonList)



            # loader()
            con.close()
        except Exception as es:
            messagebox.showerror("Error", f"Erreur due a : {str(es)}", parent=home)

def selectAll():
    for checkbutton in chBList:
        checkbutton.select()
    chBListener()

def deselectAll():
    for checkbutton in chBList:
        checkbutton.deselect()
    chBListener()

def extractData(date):
    selectedData =[]
    for dj in date:

        for d in data:
            jour = d["date"][:2]
            if jour==dj:
                selectedData.append(d)

    # print(len(selectedData))
    # print(f"Selected data:{selectedData}")
    sqlQuery(selectedData)

def sqlQuery(*args):
    global con
    global cur
    if len(args) == 0:
        valid()
    else:
        data = args[0]
        if chbutton.get() == 1:
            print("transaction mode")
            global dateCom


        for d in data:
            dateOld = d["date"]
            #convert date
            date = dateOld[6:]+"-"+dateOld[3:5]+"-"+dateOld[:2]
            casPositifs = d["casPositifs"]
            casImportes = d["casImportes"]
            casContacts = d["casContacts"]
            testRealises = d["testRealises"]
            sousTraitement = d["sousTraitement"]
            casCommunautaires = d["casCommunautaires"]
            casGueris = d["casGueris"]
            deces = d["deces"]

            localites = d["localites"][0]
            print(localites)

            sql1=f"insert into communique values('{date}',{casPositifs},{casImportes},{casContacts},{testRealises},{sousTraitement},{casCommunautaires},{casGueris},{deces})"

            try:
                cur.execute(sql1)
                if chbutton.get() == 1:
                    dateCom.append(date)
            except Exception as e:
                messagebox.showerror("Error in sqlQuery", f"Erreur in sqlQuery  due a : {str(e)}", parent=home)
            for name, value in localites.items():
                print(f"{name}: {value}\t")
                sql2 = f"insert into localites values(null,'{name}',{value})"
                try:
                    cur.execute(sql2)
                    # Apres insertion dans localites on recupere id_localite et l'inserer dans ligne_com_local
                    sql3 = f"insert into ligne_com_local values('{date}', (select id_localite from localites order by id_localite desc limit 1))"
                    cur.execute(sql3)
                except Exception as e:
                    messagebox.showerror("Error in sqlQuery", f"Erreur in sqlQuery  due a : {str(e)}", parent=home)
        con.commit()
        messagebox.showinfo("Success", "Importation vers la base reusi", parent=home)
        deselectAll()
        # enable validate and cancel buttons
        # buttonValid.configure(state=tk.NORMAL)
        buttonCancel.configure(state=NORMAL)

def getMysqlConn():
    global curs
    if  curs is None or curs.connection.close:
        try:
           curs = pymysql.connect(host="localhost", user=user_id.get(), password=user_password.get(), database="covid").cursor()
           return curs
        except Exception as e:
            messagebox.showerror("Error", f"Erreur due a : {str(e)}", parent=home)
    else:
        return curs
def insertData(sql1,sql2, cur):

    try:
            cur.execute(sql1)
            cur.execute(sql2)
    except Exception as e:
        messagebox.showerror("Error", f"Erreur due a : {str(e)}", parent=home)

def valid():
    result = messagebox.askquestion("Valider", "Etes vous sure de valider toutes vos importations?", icon='warning')
    if result == 'yes':
        print("Import")
        global con
        try:
            cur.execute("select * from communique order by date desc limit 1")
            row = cur.fetchone()
            print(f"in Valid: {row}")
            # con.ping()
            con.commit()
            con.close()
            messagebox.Message("Operation Validé", parent=home).show()
        except Exception as e:
            messagebox.showerror("Error", f"Erreur in valid due a : {str(e)}", parent=home)
    else:
        print("Cancel")



def cancels():
    result = messagebox.askquestion("Annuler", "Etes vous sure d'annuler toutes vos importations?", icon='warning')
    if result == 'yes':
        try:
            con = pymysql.connect(host="localhost", user=user_id.get(), password=user_password.get(), database="covid",
                                  port=3308)
            cur = con.cursor()
            for date in dateCom:
                sql = f"DELETE FROM communique, localite USING communique INNER JOIN localite WHERE date = '{date}' AND localite.id_localite = communique.id_localite"
                print(sql)
                cur.execute(sql)
                con.commit()
                dateCom.clear()
                print(f"List {dateCom}")
            messagebox.showinfo("Success", "L'annulation reussi", parent=home)
        except Exception as e:
            messagebox.showerror("Error", f"Erreur due a : {str(e)}", parent=home)
    else:
        print("no")

def chBListener():
    checked = False
    for i in range(len(chBvar)):
        if chBvar[i].get() == 1:
            checked = True
    if checked == True:
        buttonImport.configure(state= NORMAL)
    else:
        buttonImport.configure(state= DISABLED)


#Bar de menu
menubar = Menu(home)
filemenu = Menu(menubar, tearoff=0)
menu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Connexion")
filemenu.add_command(label="Quitter")
menubar.add_cascade(label="File", menu=filemenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help")
helpmenu.add_command(label="About")
menubar.add_cascade(label="Help", menu=helpmenu)
home.config(menu=menubar)

#Label Covid
label_covid = Label(image_label, text="COVID 19 MODELER", font = "Helvetica 18 bold", bg="#00184A",fg="white")
label_covid.place(x=getWidth(40), y=getHeight(1))

#Tabs
my_notebook = ttk.Notebook(home)
frameLoader = Frame(my_notebook, width= getWidth(80), height=getHeight(80),bg="#28527a")
frameExplorer = Frame(my_notebook, width= getWidth(80), height=getHeight(80), bg="gray")
frameAnalyser = Frame(my_notebook, width= getWidth(80), height=getHeight(80), bg="gray")
frameLoader.pack(fill ="both", expand = 1)
frameExplorer.pack(fill ="both", expand = 1)
frameAnalyser.pack(fill ="both", expand = 1)
my_notebook.add(frameLoader, text ='DATA LOADER')
my_notebook.add(frameExplorer, text ='DATA EXPLORER')
my_notebook.add(frameAnalyser, text ='DATA ANALYSER')
label_covid.update()
my_notebook.place(x=widthOfWindow/2-getWidth(80)/2,y=heightOfWindow/2-getHeight(80)/2-label_covid.winfo_height())
# m y_notebook.pack(fill=BOTH, expand=True)
#######################frameLoader design####################
labImport = Label(frameLoader, text="Import Data to Database", bg="#28527a",fg="white")
labImport.grid(row=0, columnspan=2, pady=15)
#update frame size
frameLoader.update()
#       FrameLoaderLeft
frameLoaderLeft = Frame(frameLoader, width=frameLoader.winfo_width()/2, height = frameLoader.winfo_height()*0.9,bg="#28527a")
frameLoaderRight = Frame(frameLoader, width=frameLoader.winfo_width()/2, height = frameLoader.winfo_height()*0.90,bg="#28527a")
frameLoaderLeft.grid(row= 1, column= 0)
frameLoaderRight.grid(row= 1, column= 1)
frameLoaderLeft.grid_propagate(0)
labFileSelect = Label(frameLoaderLeft, text="Select a Json file",bg="#28527a",fg="white")
buttonFileSelect = Button(frameLoaderLeft, text= "  Select  ",bg="#28527a",fg="white", command=browseFiles)
labfilename = Label(frameLoaderLeft, text="",bg="#28527a",fg="white")
frameLoaderLeft.update()
labFileSelect.place(x= frameLoaderLeft.winfo_width()/2, y=frameLoaderLeft.winfo_height()/2)
labFileSelect.update()
buttonFileSelect.place(x=frameLoaderLeft.winfo_width()/2+labFileSelect.winfo_width()+50,  y=frameLoaderLeft.winfo_height()/2)
labfilename.place(x=frameLoaderLeft.winfo_width()/2, y=frameLoaderLeft.winfo_height()/2+60)

#       FrameLoaderRight
frameLoaderRight.pack_propagate(0)
frameLoaderRight.update()
labImpDays = Label(frameLoaderRight, text="Select day(s) to import",bg="#28527a",fg="white")
labImpDays.place(x=frameLoaderRight.winfo_width()/2, y=20)
buttonImport = Button(frameLoaderRight, text="  Import  ", command=DrawImportAuthFrame, bg="#28527a", fg="white", state=DISABLED)
buttonValid = Button(frameLoaderRight, text="  Validate  ", command=sqlQuery ,bg="#28527a",fg="white", state=DISABLED)
buttonCancel = Button(frameLoaderRight, text= "  Cancel  ",bg="#28527a",fg="white", command=cancels, state=DISABLED)
buttonSelectAll = Button(frameLoaderRight, text= "    Select All    ",bg="#28527a",fg="white", command=selectAll, state= DISABLED)
buttonDeselect = Button(frameLoaderRight, text=" Deselect All  ", bg="#28527a", fg="white", command=deselectAll, state=DISABLED)



buttonCancel.place(x=250, y= frameLoaderRight.winfo_height()-50)
buttonImport.place(x=350, y= frameLoaderRight.winfo_height()-50)
buttonValid.place(x=450, y= frameLoaderRight.winfo_height()-50)
buttonSelectAll.place(x=500, y=frameLoaderRight.winfo_height()/2-50)
buttonDeselect.place(x=500, y=frameLoaderRight.winfo_height() / 2)


# Frame explorer

buttonExecute = Button(frameExplorer, text="Explore", command= DrawExploreAuthFrame)
frameExplorer.update()
buttonExecute.place(x=widthOfWindow/2-150,  y=heightOfWindow/2-110)
explorerLabel = Label(frameExplorer, text='Click button to explore data in the map')
explorerLabel.place(x=getWidth(40)-100, y=getHeight(1))
# explorerLabel.grid(row=0, columnspan=2, pady=15, padx = 15)
# buttonExecute.grid(row=1, column = 0)
# frameExplorer.grid(row = 1, column = 0)



home.mainloop()