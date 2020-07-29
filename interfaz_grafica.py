from tkinter import *
from tkinter import Tk

import cap_codigo_qr
from cap_photo_camera import cap_foto

#from visionAPI import reconocer_caras as reconocimiento
#________________Global variables____________________
#Used in part 1
global info_qr
info_qr = ""

#Used in part 2
global cedula
global curso
cedula = ""
curso = ""

#Used in part 3
global recon
recon = None

#______________Functions_____________________________
def cap_qr():#Used in page 1
    global info_qr
    global root_1

    cap_codigo_qr.qr()
    info_qr = cap_codigo_qr.data#To be able for use the ID values in every part.

    if info_qr != "":
        root_1.destroy()
        page2()

def change_info_id_cur(ced,cur):#Used in page 2
    cedula = ced
    curso = cur
    
    root_2.destroy()
    page3()

def upload_photo():#Used in page 3
    pass

def take_photo():#Used in page 3
    cap_foto()
    """Por acá quedé, estoy teniendo problemas con la captura y guardado de la imagen para su posterior envio
    al API de Google"""
#____________________________________________________
def page1():
    """Here is locate the first page of the program, in where we show the QR code to be identificade."""

    global root_1

    root_1 = Tk()
    root_1.title("Computer Vision Assistance Register")
    root_1.geometry("400x250")

    #This is used to insert text in the page.
    text_bot_qr = Text(root_1)
    text_bot_qr.insert(INSERT,"Coloque el código QR en frente de la cámara \n y luego precione el boton de abajo")
    text_bot_qr.grid(row = 0, column = 0, columnspan = 2)
    #___________________Botoms_________________________

    boton_cod_qr = Button(root_1, text = "Press here", command = cap_qr)
    boton_cod_qr.grid(row = 0, column = 0)
    root_1.mainloop()

def page2():
    """The second page is where the user can modify his information (ID)"""
    global cedula
    global curso
    global root_2

    root_2 = Tk()
    root_2.title("Computer Vision Assistance Register")    
    root_2.geometry("150x100")
    
    info = info_qr.split("#")
    cedula = info[0]
    curso = info[1]
    #Referent to the ID
    entry_ced = Entry(root_2)
    entry_ced.insert(0,cedula)
    entry_ced.grid(row = 0, column = 0, columnspan = 2)
    #Referent to the course
    entry_cur = Entry(root_2)
    entry_cur.insert(0, curso)
    entry_cur.grid(row = 1, column = 0, columnspan = 2)

    enter_button = Button(root_2, text = "Enter",
                command = lambda: change_info_id_cur(entry_ced.get(),entry_cur.get()))
    enter_button.grid(row = 2, column = 0, columnspan = 2)
    

    root_2.mainloop()
    exit()#Momentaneo hasta que pasemos a una nueva página

def page3():
    """In this part is where the system gives to the user the option to upload a photo or take a photo for
    the emotion register."""
    global root_3

    root_3 = Tk()
    root_3.title("Computer Vision Assistance Register")    

    indication = Text(root_3, width = 55, height = 5)
    indication.insert(INSERT,"¿Desea subir una foto o tomar una foto para el reporte?")
    indication.grid(row = 0, column = 0, columnspan = 2)

    upload_buttom = Button(root_3, text = "Upload photo")
    upload_buttom.grid(row = 0, column = 0)

    take_buttom = Button(root_3, text = "Take photo", command = take_photo)
    take_buttom.grid(row = 0, column = 1)

    root_3.mainloop()

#page1()
page3()