import  pickle

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

global listaCursos
listaCursos={"Taller52":None,"Intro52":None}


def registrarAsistencia (curso,cedula,fecha,emociones):
    raizAsistencia=listaCursos[curso]
    if raizAsistencia==None:
        listaCursos[curso]=asistencia(cedula)
        listaCursos[curso].crearRegistroAsistencia(cedula,fecha,emociones)
    else:
        raizAsistencia.crearRegistroAsistencia(cedula,fecha,emociones)

def save_info_archive():
    with open("info_arboles.pickle", "wb") as archi:
        pickle.dump(listaCursos, archi)
        archi.close()

def charge_info_archive():
    try:
        global listaCursos
        archi = open("info_arboles.pickle", "rb")
        dic_cursos = pickle.load(archi)
        listaCursos = dic_cursos
        archi.close()
    except FileNotFoundError:
        """If there are no previous registers"""
        pass


