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


listaCursos={"taller52":None,"intro52":None}


def registrarAsistencia (curso,cedula,fecha,emociones):
    raizAsistencia=listaCursos[curso]
    if raizAsistencia==None:
        listaCursos[curso]=asistencia(cedula)
        listaCursos[curso].crearRegistroAsistencia(cedula,fecha,emociones)
    else:
        raizAsistencia.crearRegistroAsistencia(cedula,fecha,emociones)


registrarAsistencia("taller52",205620727,{"dia":24, "mes":7, "año":2020},{"felicidad":0})
registrarAsistencia("taller52",205620727,{"dia":31, "mes":7, "año":2020},{"felicidad":5})
registrarAsistencia("taller52",205620727,{"dia":7, "mes":8, "año":2020},{"felicidad":6})
registrarAsistencia("taller52",205620726,{"dia":31, "mes":7, "año":2020},{"felicidad":4})
registrarAsistencia("taller52",205620728,{"dia":31, "mes":7, "año":2020},{"felicidad":3})
registrarAsistencia("taller52",205620729,{"dia":31, "mes":7, "año":2020},{"felicidad":3})
registrarAsistencia("taller52",205620727,{"dia":31, "mes":7, "año":2020},{"tristeza":2})
registrarAsistencia("intro52",205620727,{"dia":31, "mes":7, "año":2020},{"tristeza":2})