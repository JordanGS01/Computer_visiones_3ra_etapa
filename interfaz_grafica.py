from os import remove

from tkinter import *
from tkinter import Tk
from tkinter import filedialog

from Entorno_virtual_3do_proyecto import cap_codigo_qr
from Entorno_virtual_3do_proyecto import cap_photo_camera as cap
from Entorno_virtual_3do_proyecto import visionAPI as r
from Entorno_virtual_3do_proyecto import desgloce_reconocimientos as desg
from Entorno_virtual_3do_proyecto import tree_class as arbol
#________________Global variables____________________
#Used in qr_identification_page()
global info_qr, cedula, curso, recon
info_qr = ""
#Used in id_modification_page()
cedula = ""
curso = ""
#Used in take_upload_photo_page()
recon = None


#______________Buttons functions_____________________________
def cap_qr():#Used in qr_identification_page()
    """This function is used to capture and identify the information of the QR code in the taken photo."""
    global info_qr
    global root_1

    cap_codigo_qr.qr()
    info_qr = cap_codigo_qr.data#To be able for use the ID values in every part.

    if info_qr != "":
        root_1.destroy()
        remove("frame.png")
        id_modification_page()

def change_info_id_cur(ced,cur):#Used in id_modification_page()
    """This finction change and save the info of the course and the ID of the student. Finally, it close the window"""
    global cedula,curso
    cedula = ced
    curso = cur
    if curso == "Taller52":
        root_2.destroy()
        take_upload_photo_page()
    elif curso == "Intro52":
        root_2.destroy()
        take_upload_photo_page()
    else:
        print("El curso digitado no se encuentra en los registros, por favor \n"
              "intente de nuevo con uno que sí exista ('Taller52' o 'Intro52')")

def upload_photo():#Used in take_upload_photo_page()
    """Here is where we give the option to upload a photo from the actual device.
    Then, the information is send to the API of Google to do the face recognition.
    The information of the recognition (date and recognition values) are saved in variables be send to the binary tree
    where they are going to be saved."""

    root_3.filename =  filedialog.askopenfile(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    lista_reconocimientos = r.reconocer_caras(root_3.filename.name)
    fecha = lista_reconocimientos[0].get("fecha")
    rec = desg.asig_valores_estados_reconocidos(lista_reconocimientos)

    arbol.registrarAsistencia(curso,cedula,fecha,rec)
    arbol.save_info_archive()
    reports_page()

def take_photo():#Used in take_upload_photo_page()
    """This is the function that use the "Take photo" button.
     It takes a photo and send for its recognition, then save the information (date and recognition values) in variables
     for it posterior use."""
    cap.cap_foto()
    lista_reconocimientos = r.reconocer_caras("fotillo.png")
    fecha = lista_reconocimientos[0].get("fecha")
    rec = desg.asig_valores_estados_reconocidos(lista_reconocimientos)
    remove("fotillo.png")

    arbol.registrarAsistencia(curso,cedula,fecha,rec)
    arbol.save_info_archive()
    reports_page()
#____________________________________________________
#______________Report functions______________
def register_assistance_per_student():
    pass
def emotions_for_date():
    pass
def emotion_avarage_per_student_course():
    pass

#____________________________________________________
#______________Interface______________
def qr_identification_page():
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

    boton_cod_qr = Button(root_1, text = "Take photo", command = cap_qr)
    boton_cod_qr.grid(row = 0, column = 0)
    root_1.mainloop()

def id_modification_page():
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

def take_upload_photo_page():
    """In this part is where the system gives to the user the option to upload a photo or take a photo for
    the emotion register."""
    global root_3

    root_3 = Tk()
    root_3.title("Computer Vision Assistance Register")    

    indication = Text(root_3, width = 55, height = 5)
    indication.insert(INSERT,"¿Desea subir una foto o tomar una foto para el reporte?")
    indication.grid(row = 0, column = 0, columnspan = 2)

    upload_buttom = Button(root_3, text = "Upload photo", command = upload_photo)
    upload_buttom.grid(row = 0, column = 0)

    take_buttom = Button(root_3, text = "Take photo", command = take_photo)
    take_buttom.grid(row = 0, column = 1)

    root_3.mainloop()

def reports_page():
    """Here is where is create the page that shows the user the avalible report options"""
    root_4 = Tk()
    root_4.title("Computer Vision Assistance Register")

    register_for_students_button = Button(root_4, 
    text = "Registro de asistencia por estudiantes")
    register_for_students_button.grid(row = 0, column = 0)

    emotion_state_for_course_button = Button(root_4, 
    text = "Estado de emociones por fecha para un curso")
    emotion_state_for_course_button.grid(row = 1, column = 0)

    emotions_avarage_for_student_butoon = Button(root_4,
    text = "Promedio de emociones para un estudiante por curso")
    emotions_avarage_for_student_butoon.grid(row = 2, column = 0)

    root_4.mainloop()


arbol.charge_info_archive()
print(arbol.listaCursos)
qr_identification_page()
#take_upload_photo_page()