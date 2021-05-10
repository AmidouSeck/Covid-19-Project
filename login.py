# import tkinter as Tk
from tkinter import *
from tkinter import ttk, messagebox
import os
import pymysql


# global
from PIL import ImageTk, Image

win = Tk()
widthOfScreen = win.winfo_screenwidth()
heightOfScreen = win.winfo_screenheight()
widthOfWindow = win.winfo_screenwidth()
heightOfWindow = win.winfo_screenheight()
x_coordinate = (widthOfScreen / 2) - (widthOfWindow / 2)
y_coordinate = (heightOfScreen / 2) - (heightOfWindow / 2)
win.title('COVID 19 MODELER')
win.geometry("%dx%d+%d+%d" % (widthOfWindow, heightOfWindow, x_coordinate, y_coordinate))
win.iconbitmap('image\\icon.ico')
my_image = ImageTk.PhotoImage(Image.open('image\\homePage.jpg'))
image_label= Label(image= my_image, width=widthOfWindow, height=heightOfWindow)
image_label.pack()

# Functions
# def home
def load():
    path_explore = os.path.join(os.getcwd(), "main.py")
    os.system(f'python {path_explore}')


# test of auth function
def loginAuth():
    if user_name.get() == "" or password.get() == "":
        messagebox.showerror("Erreur", "Veillez entrer un ID et un mot de passe", parent=win)
    else:
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="mysql")
            cur = con.cursor()

            print(cur.execute("select user from user where user='" + user_name.get() + "' and authentication_string= CONCAT('*',UPPER(SHA1(UNHEX(SHA1('" + password.get() + "')))))"))

            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Erreur", "Identifiant ou mot de passe invalide", parent=win)
            else:
                messagebox.showinfo("Success", "Bienvenue", parent=win)
                win.destroy()
                load()
            # load()

            # loader()
            con.close()
        except Exception as es:
            messagebox.showerror("Error", f"Erreur due a : {str(es)}", parent=win)


# Clear function for login form
def clear():
    userentry.delete(0, END)
    passentry.delete(0, END)


# disconnect function
def disconnect():
    pass


# heading label

heading = Label(win, text="AUTHENTIFICATION", font='Verdana 30 bold')
heading.place(x=widthOfWindow/2 -200, y= heightOfWindow/2 -200)

username = Label(win, text="Login ID:", font='Verdana 10 bold')
username.place(x=widthOfWindow/2 -200, y=heightOfWindow/2 -80)

userpass = Label(win, text="Password:", font='Verdana 10 bold')
userpass.place(x=widthOfWindow/2 -200, y=heightOfWindow/2 -40)

# Entry Box
user_name = StringVar()
password = StringVar()
userentry = Entry(win, width=40, textvariable=user_name)
userentry.focus()
userentry.place(x=widthOfWindow/2 -80, y=heightOfWindow/2 -80)

passentry = Entry(win, width=40, show="*", textvariable=password)
passentry.place(x=widthOfWindow/2 -80, y=heightOfWindow/2 -40)

# button login and clear

btn_login = Button(win, text="Login", font='Verdana 10 bold', command=loginAuth)
btn_login.place(x=widthOfWindow/2 -80, y=heightOfWindow/2)

btn_login = Button(win, text="Clear", font='Verdana 10 bold', command=clear)
btn_login.place(x=widthOfWindow/2 -10, y=heightOfWindow/2)

win.mainloop()
