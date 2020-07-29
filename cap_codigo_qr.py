import cv2

"""Este código captura una imagen llamada "frame.png" que es guardada en la carpeta donde es encuentra el
archivo .py, esa imagen es utilizada para capturar un código QR y reconocerlo, para poder leer los datos
detrás de dicho código"""

global data
data = ""
#Captura de fotografía basado en la cámara
def qr():
    global data
    cap = cv2.VideoCapture(0)
    leido, frame = cap.read()
    if leido == True:
        cv2.imwrite("frame.png",frame)
        print("Foto tomada con éxito")
    else:
        print("Error al acceder a la cámara.")
    cap.release()

    #Reconocimiento de imagen con código QR
    img = cv2.imread(r'frame.png')
    detector = cv2.QRCodeDetector()
    data, points, stight_code = detector.detectAndDecode(img)
    return data
    