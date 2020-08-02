import os, io
from google.cloud import vision
from google.cloud.vision import types
from datetime import datetime

os.environ['GOOGLE_APPLICATION_CREDENTIALS']= r'key.json'
client=vision.ImageAnnotatorClient()


def reconocer_caras(url):

    with io.open(url,'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.face_detection(image=image)

    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')
    
    #lista simplificada de rostros con datos simplificados
    faces_list=[]
    for face in faces:
        #dicccionario con los angulos asociados a la detección de la cara
        face_angles=dict(roll_angle=face.roll_angle,pan_angle=face.pan_angle,tilt_angle=face.tilt_angle)
        
        #confianza de detección (tipo float)
        detection_confidence=face.detection_confidence

        #Probabilidad de Expresiones
        face_expressions=dict(  joy_likelihood=likelihood_name[face.joy_likelihood],
                                sorrow_likelihood=likelihood_name[face.sorrow_likelihood],
                                anger_likelihood=likelihood_name[face.anger_likelihood],
                                surprise_likelihood=likelihood_name[face.surprise_likelihood],
                                under_exposed_likelihood=likelihood_name[face.under_exposed_likelihood],
                                blurred_likelihood=likelihood_name[face.blurred_likelihood],
                                headwear_likelihood=likelihood_name[face.headwear_likelihood])

        #polígono de marco de cara
        vertices=[]
        for vertex in face.bounding_poly.vertices:
            vertices.append (dict (x=vertex.x, y=vertex.y))

        hora_actual = datetime.now()
        dic_hora = {"Hora": hora_actual.hour,"Minutos": hora_actual.minute,"Segundos":hora_actual.second}
        dic_fecha = {"Día":hora_actual.day,"Mes":hora_actual.month,"Año":hora_actual.year}
        dic_fecha_hora = {"Fecha": dic_fecha,"Hora": dic_hora}
        face_dict=dict( direccion_foto= url,
                        fecha = dic_fecha_hora,
                        face_angles=face_angles,
                        detection_confidence=detection_confidence,
                        face_expressions=face_expressions,
                        vertices=vertices
                        )
        faces_list.append(face_dict)
    #retorna lista de objetos con características del reconocimiento facial     
    return (faces_list)

