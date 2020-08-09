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
    global root_3

    root_3.filename =  filedialog.askopenfile(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    lista_reconocimientos = r.reconocer_caras(root_3.filename.name)
    fecha = lista_reconocimientos[0].get("fecha")
    rec = desg.asig_valores_estados_reconocidos(lista_reconocimientos)

    arbol.registrarAsistencia(curso,cedula,fecha,rec)
    arbol.save_info_archive()
    root_3.destroy()
    reports_page()

def take_photo():#Used in take_upload_photo_page()
    """This is the function that use the "Take photo" button.
     It takes a photo and send for its recognition, then save the information (date and recognition values) in variables
     for it posterior use."""
    global root_3
    cap.cap_foto()
    lista_reconocimientos = r.reconocer_caras("fotillo.png")
    fecha = lista_reconocimientos[0].get("fecha")
    rec = desg.asig_valores_estados_reconocidos(lista_reconocimientos)
    remove("fotillo.png")

    arbol.registrarAsistencia(curso,cedula,fecha,rec)
    arbol.save_info_archive()
    root_3.destroy()
    reports_page()
#____________________________________________________
#______________Report functions______________
def register_assistance_per_student():
    register_assistance = Tk()

    #Function of the enter_button:
    def muestra_est_y_emo_relevante():
        lista_personas = arbol.busca_fecha_curso_asistencia(curso_label_entry.get(),day_label_entry.get(),month_label_entry.get(),year_label_entry.get())
        #for est in lista_personas:
         #   print(est)
        ced_label = Label(register_assistance, text = "Cedulas", relief=SOLID)
        ced_label.grid(row = 5, column = 0)

        emo_label = Label(register_assistance, text = "Emociones", relief=SOLID)
        emo_label.grid(row = 5, column = 1)

        #Comenzar a trabajar con el método para mostrar los datos requeridos (cedula y emocion más relevante.)
        
    #Labels with their current entry space assignation.
    curso_label = Label(register_assistance,text = "Curso")
    curso_label.grid(row = 0, column = 0)
    curso_label_entry = Entry(register_assistance)
    curso_label_entry.grid(row = 0, column = 1)

    day_label = Label(register_assistance, text="Day")
    day_label.grid(row = 1, column = 0)
    day_label_entry = Entry(register_assistance)
    day_label_entry.grid(row = 1, column=1)

    month_label = Label(register_assistance, text="Month")
    month_label.grid(row = 2, column = 0)
    month_label_entry = Entry(register_assistance)
    month_label_entry.grid(row = 2, column = 1)

    year_label = Label(register_assistance, text = "Year")
    year_label.grid(row = 3, column = 0)
    year_label_entry = Entry(register_assistance)
    year_label_entry.grid(row = 3, column = 1)
    #End of labels and entry spaces

    #Buttons
    enter_button = Button(register_assistance, text = "Enter", command = muestra_est_y_emo_relevante)
    enter_button.grid(row = 4, column = 1)

    exit_button = Button(register_assistance, text = "Exit", command = lambda: register_assistance.destroy())
    exit_button.grid(row = 4, column = 0)

    register_assistance.mainloop()

def emotions_for_date():
    emotions_date = Tk()
#Creation of labels and buttons
    course_label = Label(emotions_date,text = "Curso:")
    course_label.grid(row = 0, column = 0)
    course_entry = Entry(emotions_date)
    course_entry.grid(row = 0, column = 1)

    day_label = Label(emotions_date, text="Día:")
    day_label.grid(row=1, column=0)
    day_entry = Entry(emotions_date)
    day_entry.grid(row=1, column=1)

    month_label = Label(emotions_date, text="Mes:")
    month_label.grid(row=2, column=0)
    month_entry = Entry(emotions_date)
    month_entry.grid(row=2, column=1)

    year_label = Label(emotions_date, text="Año:")
    year_label.grid(row=3, column=0)
    year_entry = Entry(emotions_date)
    year_entry.grid(row=3, column=1)

    enter_button = Button(emotions_date, text = "Enter", command = lambda: promedio(course_entry.get(),
                                                        day_entry.get(),month_entry.get(),year_entry.get()))
    enter_button.grid(row = 4, column = 1)

    exit_button = Button (emotions_date, text = "Exit", command = lambda: emotions_date.destroy())
    exit_button.grid(row = 4, column = 0)
#End of the creation of labels and entries spaces
    def promedio(curso,dia,mes,año):
        asis_values = arbol.busca_fecha_curso(curso,dia,mes,año)
        #________________________________________________________
        try:
            global joy, joy_value, sorrow, sorrow_value, anger, anger_value, surprised, surprised_value, under_exposed, under_exposed_value, blurred, blurred_value, headwear, headwear_value
            joy.grid_forget()
            joy_value.grid_forget()
            sorrow.grid_forget()
            sorrow_value.grid_forget()
            anger.grid_forget()
            anger_value.grid_forget()
            surprised.grid_forget()
            surprised_value.grid_forget()
            under_exposed.grid_forget()
            under_exposed_value.grid_forget()
            blurred.grid_forget()
            blurred_value.grid_forget()
            headwear.grid_forget()
            headwear_value.grid_forget()

            exit_button = Button(emotions_date, text="Exit", command=lambda: emotions_date.destroy())
            exit_button.grid(row=4, column=0)

            curso_label = Label(emotions_date, text=curso, relief=SOLID)
            curso_label.grid(row=5, column=0)

            joy = Label(emotions_date, text="Joy:", relief=GROOVE)
            joy.grid(row=6, column=0)
            joy_value = Label(emotions_date, text="{0}{1}".format(asis_values[0], "%"))
            joy_value.grid(row=7, column=0)

            sorrow = Label(emotions_date, text="Sorrow:", relief=GROOVE)
            sorrow.grid(row=8, column=0)
            sorrow_value = Label(emotions_date, text="{0}{1}".format(asis_values[1], "%"))
            sorrow_value.grid(row=9, column=0)

            anger = Label(emotions_date, text="Anger:", relief=GROOVE)
            anger.grid(row=10, column=0)
            anger_value = Label(emotions_date, text="{0}{1}".format(asis_values[2], "%"))
            anger_value.grid(row=11, column=0)

            surprised = Label(emotions_date, text="Surprised:", relief=GROOVE)
            surprised.grid(row=12, column=0)
            surprised_value = Label(emotions_date, text="{0}{1}".format(asis_values[3], "%"))
            surprised_value.grid(row=13, column=0)

            under_exposed = Label(emotions_date, text="Under Exposed:", relief=GROOVE)
            under_exposed.grid(row=14, column=0)
            under_exposed_value = Label(emotions_date, text="{0}{1}".format(asis_values[4], "%"))
            under_exposed_value.grid(row=15, column=0)

            blurred = Label(emotions_date, text="Blurred:", relief=GROOVE)
            blurred.grid(row=16, column=0)
            blurred_value = Label(emotions_date, text="{0}{1}".format(asis_values[5], "%"))
            blurred_value.grid(row=17, column=0)

            headwear = Label(emotions_date, text="Headwear:", relief=GROOVE)
            headwear.grid(row=18, column=0)
            headwear_value = Label(emotions_date, text="{0}{1}".format(asis_values[6], "%"))
            headwear_value.grid(row=19, column=0)

        except NameError:
            try:
                curso_label = Label(emotions_date, text=curso, relief=SOLID)
                curso_label.grid(row=4, column=0)

                exit_button = Button(emotions_date, text="Exit", command=lambda: emotions_date.destroy())
                exit_button.grid(row=4, column=0)

                joy = Label(emotions_date, text="Joy:", relief=GROOVE)
                joy.grid(row=5, column=0)
                joy_value = Label(emotions_date, text="{0}{1}".format(asis_values[0], "%"))
                joy_value.grid(row=6, column=0)

                sorrow = Label(emotions_date, text="Sorrow:", relief=GROOVE)
                sorrow.grid(row=7, column=0)
                sorrow_value = Label(emotions_date, text="{0}{1}".format(asis_values[1], "%"))
                sorrow_value.grid(row=8, column=0)

                anger = Label(emotions_date, text="Anger:", relief=GROOVE)
                anger.grid(row=9, column=0)
                anger_value = Label(emotions_date, text="{0}{1}".format(asis_values[2], "%"))
                anger_value.grid(row=10, column=0)

                surprised = Label(emotions_date, text="Surprised:", relief=GROOVE)
                surprised.grid(row=11, column=0)
                surprised_value = Label(emotions_date, text="{0}{1}".format(asis_values[3], "%"))
                surprised_value.grid(row=12, column=0)

                under_exposed = Label(emotions_date, text="Under Exposed:", relief=GROOVE)
                under_exposed.grid(row=13, column=0)
                under_exposed_value = Label(emotions_date, text="{0}{1}".format(asis_values[4], "%"))
                under_exposed_value.grid(row=14, column=0)

                blurred = Label(emotions_date, text="Blurred:", relief=GROOVE)
                blurred.grid(row=15, column=0)
                blurred_value = Label(emotions_date, text="{0}{1}".format(asis_values[5], "%"))
                blurred_value.grid(row=16, column=0)

                headwear = Label(emotions_date, text="Headwear:", relief=GROOVE)
                headwear.grid(row=17, column=0)
                headwear_value = Label(emotions_date, text="{0}{1}".format(asis_values[6], "%"))
                headwear_value.grid(row=18, column=0)
            except TypeError:
                pass
            except TclError:
                pass

    emotions_date.mainloop()

def emotion_avarage_per_student_course():
    """Here is where take place the the 3th report available in the reports menu."""
    emotion_avarage = Tk()
    emotion_avarage.config(width = 200, height = 150)
    emotion_avarage.title("Emotion Avarage Per Student")

    #Give to the user the option to insert the ID of the student. Save the ID in a variable.
    lab = Label(emotion_avarage, text = "Cedula")
    lab.grid(row = 0, column = 0)

    ced = Entry(emotion_avarage, bd = 2)
    ced.grid(row = 0, column = 1)

    def promedicacion():
        """Here is where we use the information given for the user to print in the screen the values of the emotions of
        each course.
        Fist of all, we delete the previous widgets."""
        try:
            global joy_1,joy_1_value,sorrow_1,sorrow_1_value,anger_1,anger_1_value,surprised_1,surprised_1_value,under_exposed_1,under_exposed_1_value,blurred_1,blurred_1_value,headwear_1,headwear_1_value
            global joy_2,joy_2_value,sorrow_2,sorrow_2_value,anger_2,anger_2_value,surprised_2,surprised_2_value,under_exposed_2,under_exposed_2_value,blurred_2,blurred_2_value,headwear_2,headwear_2_value
            joy_1.grid_forget()
            joy_1_value.grid_forget()
            sorrow_1.grid_forget()
            sorrow_1_value.grid_forget()
            anger_1.grid_forget()
            anger_1_value.grid_forget()
            surprised_1.grid_forget()
            surprised_1_value.grid_forget()
            under_exposed_1.grid_forget()
            under_exposed_1_value.grid_forget()
            blurred_1.grid_forget()
            blurred_1_value.grid_forget()
            headwear_1.grid_forget()
            headwear_1_value.grid_forget()

            joy_2.grid_forget()
            joy_2_value.grid_forget()
            sorrow_2.grid_forget()
            sorrow_2_value.grid_forget()
            anger_2.grid_forget()
            anger_2_value.grid_forget()
            surprised_2.grid_forget()
            surprised_2_value.grid_forget()
            under_exposed_2.grid_forget()
            under_exposed_2_value.grid_forget()
            blurred_2.grid_forget()
            blurred_2_value.grid_forget()
            headwear_2.grid_forget()
            headwear_2_value.grid_forget()

            cedula_ingresada = ced.get()
            promediados = arbol.recorre_arbol_para_promedio_por_estudiante(cedula_ingresada, "Intro52")

            intro_label = Label(emotion_avarage, text="Introdicción52", relief=SOLID)
            intro_label.grid(row=2, column=0)

            joy_1 = Label(emotion_avarage, text="Joy:", relief=GROOVE)
            joy_1.grid(row=3, column=0)
            joy_1_value = Label(emotion_avarage, text="{0}{1}".format(promediados[0], "%"))
            joy_1_value.grid(row=4, column=0)

            sorrow_1 = Label(emotion_avarage, text="Sorrow:", relief=GROOVE)
            sorrow_1.grid(row=5, column=0)
            sorrow_1_value = Label(emotion_avarage, text="{0}{1}".format(promediados[1], "%"))
            sorrow_1_value.grid(row=6, column=0)

            anger_1 = Label(emotion_avarage, text="Anger:", relief=GROOVE)
            anger_1.grid(row=7, column=0)
            anger_1_value = Label(emotion_avarage, text="{0}{1}".format(promediados[2], "%"))
            anger_1_value.grid(row=8, column=0)

            surprised_1 = Label(emotion_avarage, text="Surprised:", relief=GROOVE)
            surprised_1.grid(row=9, column=0)
            surprised_1_value = Label(emotion_avarage, text="{0}{1}".format(promediados[3], "%"))
            surprised_1_value.grid(row=10, column=0)

            under_exposed_1 = Label(emotion_avarage, text="Under Exposed:", relief=GROOVE)
            under_exposed_1.grid(row=11, column=0)
            under_exposed_1_value = Label(emotion_avarage, text="{0}{1}".format(promediados[4], "%"))
            under_exposed_1_value.grid(row=12, column=0)

            blurred_1 = Label(emotion_avarage, text="Blurred:", relief=GROOVE)
            blurred_1.grid(row=13, column=0)
            blurred_1_value = Label(emotion_avarage, text="{0}{1}".format(promediados[5], "%"))
            blurred_1_value.grid(row=14, column=0)

            headwear_1 = Label(emotion_avarage, text="Headwear:", relief=GROOVE)
            headwear_1.grid(row=15, column=0)
            headwear_1_value = Label(emotion_avarage, text="{0}{1}".format(promediados[6], "%"))
            headwear_1_value.grid(row=16, column=0)

            # TALLER
            promediados = arbol.recorre_arbol_para_promedio_por_estudiante(cedula_ingresada, "Taller52")

            taller_label = Label(emotion_avarage, text="Taller52", relief=SOLID)
            taller_label.grid(row=2, column=1)

            joy_2 = Label(emotion_avarage, text="Joy:", relief=GROOVE)
            joy_2.grid(row=3, column=1)
            joy_2_value = Label(emotion_avarage, text="{0}{1}".format(promediados[0], "%"))
            joy_2_value.grid(row=4, column=1)

            sorrow_2 = Label(emotion_avarage, text="Sorrow:", relief=GROOVE)
            sorrow_2.grid(row=5, column=1)
            sorrow_2_value = Label(emotion_avarage, text="{0}{1}".format(promediados[1], "%"))
            sorrow_2_value.grid(row=6, column=1)

            anger_2 = Label(emotion_avarage, text="Anger:", relief=GROOVE)
            anger_2.grid(row=7, column=1)
            anger_2_value = Label(emotion_avarage, text="{0}{1}".format(promediados[2], "%"))
            anger_2_value.grid(row=8, column=1)

            surprised_2 = Label(emotion_avarage, text="Surprised:", relief=GROOVE)
            surprised_2.grid(row=9, column=1)
            surprised_2_value = Label(emotion_avarage, text="{0}{1}".format(promediados[3], "%"))
            surprised_2_value.grid(row=10, column=1)

            under_exposed_2 = Label(emotion_avarage, text="Under Exposed:", relief=GROOVE)
            under_exposed_2.grid(row=11, column=1)
            under_exposed_2_value = Label(emotion_avarage, text="{0}{1}".format(promediados[4], "%"))
            under_exposed_2_value.grid(row=12, column=1)

            blurred_2 = Label(emotion_avarage, text="Blurred:", relief=GROOVE)
            blurred_2.grid(row=13, column=1)
            blurred_2_value = Label(emotion_avarage, text="{0}{1}".format(promediados[5], "%"))
            blurred_2_value.grid(row=14, column=1)

            headwear_2 = Label(emotion_avarage, text="Headwear:", relief=GROOVE)
            headwear_2.grid(row=15, column=1)
            headwear_2_value = Label(emotion_avarage, text="{0}{1}".format(promediados[6], "%"))
            headwear_2_value.grid(row=16, column=1)
        except NameError:
            try:
                cedula_ingresada = ced.get()
                promediados = arbol.recorre_arbol_para_promedio_por_estudiante(cedula_ingresada, "Intro52")

                intro_label = Label(emotion_avarage, text="Introdicción52",relief = SOLID)
                intro_label.grid(row=2, column=0)

                joy_1 = Label(emotion_avarage, text="Joy:",relief = GROOVE)
                joy_1.grid(row=3, column=0)
                joy_1_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[0],"%"))
                joy_1_value.grid(row = 4, column = 0)

                sorrow_1 = Label(emotion_avarage, text="Sorrow:",relief = GROOVE)
                sorrow_1.grid(row=5, column=0)
                sorrow_1_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[1],"%"))
                sorrow_1_value.grid(row = 6, column = 0)


                anger_1 = Label(emotion_avarage, text="Anger:",relief = GROOVE)
                anger_1.grid(row=7, column=0)
                anger_1_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[2],"%"))
                anger_1_value.grid(row = 8, column = 0)


                surprised_1 = Label(emotion_avarage, text="Surprised:",relief = GROOVE)
                surprised_1.grid(row=9, column=0)
                surprised_1_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[3],"%"))
                surprised_1_value.grid(row = 10, column = 0)


                under_exposed_1 = Label(emotion_avarage, text="Under Exposed:",relief = GROOVE)
                under_exposed_1.grid(row=11, column=0)
                under_exposed_1_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[4],"%"))
                under_exposed_1_value.grid(row = 12, column = 0)


                blurred_1 = Label(emotion_avarage, text="Blurred:",relief = GROOVE)
                blurred_1.grid(row=13, column=0)
                blurred_1_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[5],"%"))
                blurred_1_value.grid(row = 14, column = 0)


                headwear_1 = Label(emotion_avarage, text="Headwear:",relief = GROOVE)
                headwear_1.grid(row=15, column=0)
                headwear_1_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[6],"%"))
                headwear_1_value.grid(row = 16, column = 0)

                # TALLER
                promediados = arbol.recorre_arbol_para_promedio_por_estudiante(cedula_ingresada, "Taller52")

                taller_label = Label(emotion_avarage, text="Taller52",relief = SOLID)
                taller_label.grid(row=2, column=1)


                joy_2 = Label(emotion_avarage, text="Joy:",relief = GROOVE)
                joy_2.grid(row = 3, column = 1)
                joy_2_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[0],"%"))
                joy_2_value.grid(row = 4, column = 1)

                sorrow_2 = Label(emotion_avarage, text="Sorrow:",relief = GROOVE)
                sorrow_2.grid(row = 5, column = 1)
                sorrow_2_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[1],"%"))
                sorrow_2_value.grid(row = 6, column = 1)


                anger_2 = Label(emotion_avarage, text="Anger:",relief = GROOVE)
                anger_2.grid(row=7, column=1)
                anger_2_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[2],"%"))
                anger_2_value.grid(row = 8, column = 1)


                surprised_2 = Label(emotion_avarage, text="Surprised:",relief = GROOVE)
                surprised_2.grid(row=9, column=1)
                surprised_2_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[3],"%"))
                surprised_2_value.grid(row = 10, column = 1)


                under_exposed_2 = Label(emotion_avarage, text="Under Exposed:",relief = GROOVE)
                under_exposed_2.grid(row=11, column=1)
                under_exposed_2_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[4],"%"))
                under_exposed_2_value.grid(row = 12, column = 1)


                blurred_2 = Label(emotion_avarage, text="Blurred:",relief = GROOVE)
                blurred_2.grid(row=13, column=1)
                blurred_2_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[5],"%"))
                blurred_2_value.grid(row = 14, column = 1)


                headwear_2 = Label(emotion_avarage, text="Headwear:",relief = GROOVE)
                headwear_2.grid(row=15, column=1)
                headwear_2_value = Label(emotion_avarage, text = "{0}{1}".format(promediados[6],"%"))
                headwear_2_value.grid(row = 16, column = 1)

            except TypeError:
                pass

    #This button is used to start the procedure to give the report to the user.
    enter_button = Button(emotion_avarage,text = "Enter", command = promedicacion)
    enter_button.grid(row = 1, column = 1)

    exit_button = Button(emotion_avarage, text = "Exit", command = lambda: emotion_avarage.destroy())
    exit_button.grid(row=1, column=0)


    emotion_avarage.mainloop()
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
    global root_4
    root_4 = Tk()
    root_4.title("Computer Vision Assistance Register")

    register_for_students_button = Button(root_4, 
    text = "Registro de asistencia por estudiantes", command = register_assistance_per_student)
    register_for_students_button.grid(row = 0, column = 0)

    emotion_state_for_course_button = Button(root_4, 
    text = "Estado de emociones por fecha para un curso", command = emotions_for_date)
    emotion_state_for_course_button.grid(row = 1, column = 0)

    emotions_avarage_for_student_butoon = Button(root_4,
    text = "Promedio de emociones para un estudiante por curso",  command = emotion_avarage_per_student_course)
    emotions_avarage_for_student_butoon.grid(row = 2, column = 0)

    root_4.mainloop()


#arbol.charge_info_archive()
#qr_identification_page()
reports_page()