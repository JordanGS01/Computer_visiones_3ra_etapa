import cv2

"""Este código captura una imagen llamada "fotillo.png" que es guardada en la carpeta donde es encuentra el
archivo .py, esa imagen es enviada al API de Google para la obtención de los estados de emociones del usuario."""


#Captura de fotografía basado en la cámara
def cap_foto():
    cap = cv2.VideoCapture(0)
    leido, frame = cap.read()
    if leido == True:
        cv2.imwrite("fotillo.png",frame)
        print("Foto tomada con éxito")
    else:
        print("Error al acceder a la cámara.")
    cap.release()
