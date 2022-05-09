from tkinter import *
# from tkinter import messagebox
# from tkinter import ttk
# from tkinter import simpledialog
# # import xlwt
# import webbrowser
# # from xlwt import Workbook
# import math
# import pickle
# from tkinter import filedialog
# import os

from funciones import *

# colores a utilizar-------------------------------------
azul_oscuro = "#2f354a"
azul_medio = "#1b5998"
naranja = "#fe9870"
claro = "#f2eddf"
fuente = ("Verdana", 10)
nombre = "Diseño Flujo Libre"

# ----------------Interfaz gráfica-----------------------------

raiz = Tk()
raiz.title(nombre)
# raiz.iconbitmap('road16px.ico')

barraMenu = Menu(raiz, font=fuente)
raiz.config(menu=barraMenu, bg=azul_oscuro)

ancho_programa = 1200
alto_programa = 500

ws = raiz.winfo_screenwidth()  # ancho pantalla
hs = raiz.winfo_screenheight()  # alto pantalla

x = ws / 2 - ancho_programa / 2
y = hs / 2 - alto_programa / 2

raiz.geometry('%dx%d+%d+%d' % (ancho_programa, alto_programa, x, y))

frame1 = Frame(raiz, width=500, height=500, bg=azul_oscuro)
frame2 = Frame(raiz, width=700, height=500, bg=azul_oscuro)
# frame3 = Frame(frame2, width=350, height=80, bg=azul_oscuro)
# frame4 = Frame(frame2, bg=azul_oscuro)

# frame1.config(width=350, height=310)
# frame2.config(width=350, height=310)

frame1.pack(side="left")
frame2.pack(side="left")
# frame3.pack()
# frame4.pack()

frame1.config(bd=10, relief="groove")
frame2.config(bd=10, relief="groove")

#  Entrada de caudal
QLabel = Label(frame1, text="Caudal (L/s):", bg=azul_oscuro, fg=claro, font=fuente)
QLabel.place(x=10, y=30)
entQ = Entry(frame1, width=8, justify="right", bg=azul_medio, fg=claro, font=fuente)
entQ.place(x=180, y=30)

#  Entrada de cota superior
cotaSupLabel = Label(frame1, text="Cota superior (m):", bg=azul_oscuro, fg=claro, font=fuente)
cotaSupLabel.place(x=10, y=80)
entCotaSup = Entry(frame1, width=8, justify="right", bg=azul_medio, fg=claro, font=fuente)
entCotaSup.place(x=180, y=80)

#  Entrada de cota inferior
cotaInfLabel = Label(frame1, text="Cota inferior (m):", bg=azul_oscuro, fg=claro, font=fuente)
cotaInfLabel.place(x=10, y=130)
entCotaInf = Entry(frame1, width=8, justify="right", bg=azul_medio, fg=claro, font=fuente)
entCotaInf.place(x=180, y=130)

#  Entrada de longitud
longLabel = Label(frame1, text="Longitud (m):", bg=azul_oscuro, fg=claro, font=fuente)
longLabel.place(x=10, y=180)
entlong = Entry(frame1, width=8, justify="right", bg=azul_medio, fg=claro, font=fuente)
entlong.place(x=180, y=180)

# Entrada de material PVC o concreto
varOpcionMat = BooleanVar()

materialLabel = Label(frame1, text="Material:", bg=azul_oscuro, fg=claro, font=fuente)
materialLabel.place(x=10, y=230)

rbutMatConc = Radiobutton(frame1, text="Concreto", variable=varOpcionMat,
                          value=False, bg=azul_oscuro, fg=claro, font=fuente)
rbutMatConc.config(activebackground=azul_oscuro, activeforeground=claro, selectcolor=azul_medio)
rbutMatConc.place(x=180, y=230)
rbutMatPVC = Radiobutton(frame1, text="PVC", variable=varOpcionMat, value=True, bg=azul_oscuro, fg=claro, font=fuente)
rbutMatPVC.config(activebackground=azul_oscuro, activeforeground=claro, selectcolor=azul_medio)
rbutMatPVC.place(x=180, y=260)

# ----------------Botón de calcular-----------------------------
botCalcular = Button(frame1, text="Calcular", width=10,
                     command=lambda: setTextLabelSalida())
botCalcular.config(bg=claro, fg=azul_oscuro, activebackground=azul_oscuro, activeforeground=claro, font=fuente)
botCalcular.place(x=180, y=330)

# Label de salidas--------------------------------------
salidasLabel = Label(frame2, text="",
                     bg=azul_oscuro, fg=claro, font=fuente, wraplength=1500, justify=LEFT)
salidasLabel.place(x=10, y=10)


def setTextLabelSalida():
    texto = calcular(float(entQ.get()), float(entCotaSup.get()),
                     float(entCotaInf.get()), float(entlong.get()), varOpcionMat.get())
    salidasLabel.config(text=texto)


raiz.mainloop()
