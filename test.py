from tkinter import *
#
# def sel():
#    selection = "You selected the option " + str(var.get())
#    label.config(text = selection)
#
# root = Tk()
# var = IntVar()
# R1 = Radiobutton(root, text="Option 1", variable=var, value=1,
#                   command=sel)
# R1.pack( anchor = W )
#
# R2 = Radiobutton(root, text="Option 2", variable=var, value=2,
#                   command=sel)
# R2.pack( anchor = W )
#
# R3 = Radiobutton(root, text="Option 3", variable=var, value=3,
#                   command=sel)
# R3.pack( anchor = W)
#
# label = Label(root)
# label.pack()
# root.mainloop()

# import tkinter as tk
#
# class FullScreenApp(object):
#     def __init__(self, master, **kwargs):
#         self.master=master
#         pad=0
#         self._geom='200x200+0+0'
#         master.geometry("{0}x{1}+0+0".format(
#             master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
#         master.bind('<Escape>',self.toggle_geom)
#     def toggle_geom(self,event):
#         geom=self.master.winfo_geometry()
#         print(geom,self._geom)
#         self.master.geometry(self._geom)
#         self._geom=geom
#
# root=tk.Tk()
# app=FullScreenApp(root)
# root.mainloop()
from tkinter import messagebox
home=Tk()
# Configuration de la page d'acceuil
# home.configure(bg="blue")
#Constants
home.update()
widthOfScreen = home.winfo_screenwidth()
heightOfScreen = home.winfo_screenheight()
widthOfWindow = 500
heightOfWindow = 500

x_coordinate = (widthOfScreen/2)-(widthOfWindow/2)
y_coordinate = (heightOfScreen/2)-(heightOfWindow/2)
x_coordinate = 0
y_coordinate = 0
home.title('COVID 19 MODELER')
home.geometry("%dx%d+%d+%d"%(widthOfWindow,heightOfWindow,x_coordinate,y_coordinate))

home.mainloop()