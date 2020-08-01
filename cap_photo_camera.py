import cv2

"""This code take a photo and call it "fotillo.png" and send it to the API of Google to do the face recognition
"""

#Captura de fotografía basado en la cámara
def cap_foto():
    cap = cv2.VideoCapture(0)
    leido, frame = cap.read()
    if leido == True:
        cv2.imwrite("fotillo.png", frame)
        print("Foto tomada con éxito")
    else:
        print("Error al acceder a la cámara.")
    cap.release()

