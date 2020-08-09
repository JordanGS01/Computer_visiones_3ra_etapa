import  pickle
from operator import itemgetter

global listaCursos
listaCursos = {"Taller52":None,"Intro52":None}

class registroAsistencia():
    """Registro de asistencia
    """
    fecha=None
    emociones=None
    sig=None
    def __init__(self,fecha,emociones):
        """Constructor de los registros de emociones

        Args:
            fecha (dict): Fecha del registro
            emociones (dict): Emociones reconocidas por el API google-cloud-vision
        """
        self.fecha=fecha
        self.emociones=emociones

    def insertaRegistro(self,fecha,emociones):
        if self.sig==None:
            self.sig=registroAsistencia(fecha,emociones)
        else:
            self.sig.insertaRegistro(fecha,emociones)

class asistencia():
    cedula=None
    iz=None
    der=None
    asistencia=None
    def __init__(self,cedula):
        self.cedula=cedula

    def crearRegistroAsistencia (self,cedula,fecha,emociones):
        if self.cedula==cedula:
            if self.asistencia==None:
                self.asistencia=registroAsistencia(fecha,emociones)
            else:
                self.asistencia.insertaRegistro(fecha,emociones)
        elif self.cedula>cedula:
            if self.iz==None:
                self.iz=asistencia(cedula)
                self.iz.asistencia=registroAsistencia(fecha,emociones)
            else:
                self.iz.crearRegistroAsistencia(cedula,fecha,emociones)
        else:
            if self.der==None:
                self.der=asistencia(cedula)
                self.der.asistencia=registroAsistencia(fecha,emociones)
            else:
                self.der.crearRegistroAsistencia(cedula,fecha,emociones)

def registrarAsistencia (curso,cedula,fecha,emociones):
    raizAsistencia=listaCursos[curso]
    if raizAsistencia==None:
        listaCursos[curso]=asistencia(cedula)
        listaCursos[curso].crearRegistroAsistencia(cedula,fecha,emociones)
    else:
        raizAsistencia.crearRegistroAsistencia(cedula,fecha,emociones)

#_______Assistance_register_______
def busca_fecha_curso_asistencia(curso,dia,mes,año):
    """Create a list in where the students and their more relevant emotion will be saved.
    Finally, return the list."""
    global estudiantes_presentes
    estudiantes_presentes = []

    recorre_arbol_fecha_asistencia(listaCursos.get(curso),dia,mes,año)

    return estudiantes_presentes

def recorre_arbol_fecha_asistencia(cur,dia,mes,año):
    try:
        if cur.iz == None:
            pass
        else:
            recorre_arbol_fecha_asistencia(cur.iz,dia,mes,año)

        if cur.der == None:
            pass
        else:
            recorre_arbol_fecha_asistencia(cur.der,dia,mes,año)

            """ if revisa_registros_asistencia(cur.asistencia,dia,mes,año) == True:
                global estudiantes_presentes
                """"lista_emo = [ID, [emotion_name, emotion_value]]""""
                lista_emo = [cur.cedula, busca_emocion_mas_relevante(cur.asistencia.emociones)]
                estudiantes_presentes.append(lista_emo)"""
        revisa_registros_asistencia(cur.asistencia,dia,mes,año,cur)
        if cur.asistencia.sig != None:
            revisa_registros_asistencia(cur.asistencia.sig,dia,mes,año,cur)
    except AttributeError:
        pass

def revisa_registros_asistencia(asi,dia,mes,año,cur):
    if asi.fecha.get("Fecha").get("Año") == int(año):
        if asi.fecha.get("Fecha").get("Mes") == int(mes):
            if asi.fecha.get("Fecha").get("Día") == int(dia):
                global estudiantes_presentes
                """lista_emo = [ID, [emotion_name, emotion_value]]"""
                lista_emo = [cur.cedula, busca_emocion_mas_relevante(cur.asistencia.emociones)]
                estudiantes_presentes.append(lista_emo)
            else:
                pass
        else:
            pass
    else:
        pass

def busca_emocion_mas_relevante(emociones):
    """Here we make comparisons to see what is the highest value of emotion that the student have in the introduce day"""
    emociones_ordenadas = sorted(emociones.items(),key = itemgetter(1),reverse = True)
    dic_emociones = [emociones_ordenadas[0][0], emociones_ordenadas[0][1]]
    return dic_emociones

#_______END_Assistance_register_______

#_______EMOTIONS FOR DATE FOR ONE COURSE_______
def busca_fecha_curso(curso,dia,mes,año):
    global joy, sorrow, anger, surprise, under_exposed, blurred, headwear
    joy = 0
    sorrow = 0
    anger = 0
    surprise = 0
    under_exposed = 0
    blurred = 0
    headwear = 0

    recorre_arbol_fecha(listaCursos.get(curso),dia,mes,año)

    suma_busca_fecha = joy + sorrow + anger + surprise + under_exposed + blurred + headwear

    try:
        joy = (joy/suma_busca_fecha)*100
        sorrow = (sorrow/suma_busca_fecha)*100
        anger = (anger/suma_busca_fecha)*100
        surprise = (surprise/suma_busca_fecha)*100
        under_exposed = (under_exposed/suma_busca_fecha)*100
        blurred = (blurred/suma_busca_fecha)*100
        headwear = (headwear/suma_busca_fecha)*100

        ordenados = [joy,sorrow,anger,surprise,under_exposed,blurred,headwear]
        return ordenados
    except ZeroDivisionError:
        ordenados_fech = [joy,sorrow,anger,surprise,under_exposed,blurred,headwear]
        return ordenados_fech

def recorre_arbol_fecha(cur,dia,mes,año):
    try:
        if cur.iz == None:
            pass
        else:
            recorre_arbol_fecha(cur.iz,dia,mes,año)

        if cur.der == None:
            pass
        else:
            recorre_arbol_fecha(cur.der,dia,mes,año)

        revisa_registros(cur.asistencia,dia,mes,año)
    except AttributeError:
        pass

def revisa_registros(asi,dia,mes,año):
    if asi.fecha.get("Fecha").get("Año") == int(año):
        if asi.fecha.get("Fecha").get("Mes") == int(mes):
            if asi.fecha.get("Fecha").get("Día") == int(dia):
                suma_valores_emociones_rep_2(asi,dia,mes,año)
            else:
                pass
        else:
            pass
    else:
        pass

def suma_valores_emociones_rep_2(asis,d,m,a):
    """Here is where the values of the emotions are actualize based on the current values of the registers saved.
    Var:
        asis(registroAsistencia obj): Where are saved the values of the face detections registers."""
    global joy, sorrow, anger, surprise, under_exposed, blurred, headwear
    joy += asis.emociones.get("Joy")
    sorrow += asis.emociones.get("Sorrow")
    anger += asis.emociones.get("Anger")
    surprise += asis.emociones.get("Surprise")
    under_exposed += asis.emociones.get("Under_Exposed")
    blurred += asis.emociones.get("Blurred")
    headwear += asis.emociones.get("Headwear")

    if asis.sig == None:
        pass
    else:
        revisa_registros(asis.sig,d,m,a)

#_______END_EMOTIONS FOR DATE FOR ONE COURSE_______

#______AVARAGE OF EMOTIONS FOR EACH COURSE_______
def recorre_arbol_para_promedio_por_estudiante(cedula,curso):
    """Set the values of the emotions to 0.
    Search, for each course in the list of courses, the ID of the student and then search the registers where the emotions
    values are saved. Finally, it saved the values in a list and return that list.
    Vars:
        cedula (int): the ID of the student """
    global joy,sorrow,anger,surprise,under_exposed,blurred,headwear
    joy = 0
    sorrow = 0
    anger = 0
    surprise = 0
    under_exposed = 0
    blurred = 0
    headwear = 0


    recorre_arbol_busca_reg(listaCursos.get(curso),cedula)

    sumatoria = joy + sorrow + anger + surprise + under_exposed + blurred + headwear
    try:
        joy = (joy/sumatoria)*100
        sorrow = (sorrow/sumatoria)*100
        anger = (anger/sumatoria)*100
        surprise = (surprise/sumatoria)*100
        under_exposed = (under_exposed/sumatoria)*100
        blurred = (blurred/sumatoria)*100
        headwear = (headwear/sumatoria)*100

        ordenados = [joy,sorrow,anger,surprise,under_exposed,blurred,headwear]
        return ordenados
    except ZeroDivisionError:
        ordenados = [joy,sorrow,anger,surprise,under_exposed,blurred,headwear]
        return ordenados

def recorre_arbol_busca_reg(raiz,ced):
    """Search un the tree the ID of the student. If it found it, the function start to upload the emotion values.
    Vars:
        ced(int): The ID of the student.
        raiz(asistencia obj): The begining of the tree in where we start to search."""
    try:
        if int(raiz.cedula) == None:
            pass
        elif int(raiz.cedula) == int(ced):
            suma_valores_emociones(raiz.asistencia)
        else:
            if int(raiz.cedula) > int(ced):
                recorre_arbol_busca_reg(raiz.iz,ced)
            else:
                recorre_arbol_busca_reg(raiz.der,ced)
    except ValueError:
        pass
    except AttributeError:
        pass

def suma_valores_emociones(asis):
    """Here is where the values of the emotions are actualize based on the current values of the registers saved.
    Var:
        asis(registroAsistencia obj): Where are saved the values of the face detections registers."""
    global joy, sorrow, anger, surprise, under_exposed, blurred, headwear
    joy += asis.emociones.get("Joy")
    sorrow += asis.emociones.get("Sorrow")
    anger += asis.emociones.get("Anger")
    surprise += asis.emociones.get("Surprise")
    under_exposed += asis.emociones.get("Under_Exposed")
    blurred += asis.emociones.get("Blurred")
    headwear += asis.emociones.get("Headwear")

    if asis.sig == None:
        return
    else:
        suma_valores_emociones(asis.sig)
#______END_AVARAGE OF EMOTIONS FOR EACH COURSE_______
def save_info_archive():
    """Save the information in a binary archive"""
    with open("info_arboles.pickle", "wb") as archi:
        pickle.dump(listaCursos, archi)
        archi.close()

def charge_info_archive():
    """Chargue all the previous information in the RAM"""
    try:
        global listaCursos
        archi = open("info_arboles.pickle", "rb")
        dic_cursos = pickle.load(archi)
        listaCursos = dic_cursos
        archi.close()
    except FileNotFoundError:
        """If there are no previous registers"""
        pass

charge_info_archive()


#print(listaCursos.get("Taller52").asistencia.sig.sig.sig.sig.fecha)
#print(busca_fecha_curso_asistencia("Taller52",9,8,2020))


#print(listaCursos.get("Intro52").cedula)