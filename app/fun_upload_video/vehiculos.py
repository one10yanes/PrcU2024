import cv2
from .rastreador import Rastreador  # Asegúrate de que la importación sea correcta

class Vehiculos:
    def __init__(self):
        self.rastreador = Rastreador()
        self.deteccion = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=100)

    def procesar_frame(self, frame):
        # Aplica el sustractor de fondo para obtener las áreas en movimiento
        mascara = self.deteccion.apply(frame)
        _, umbral = cv2.threshold(mascara, 254, 255, cv2.THRESH_BINARY)
        contornos, _ = cv2.findContours(umbral, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        detecciones = []
        for cnt in contornos:
            area = cv2.contourArea(cnt)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                detecciones.append([x, y, w, h])

        # Rastrea los objetos detectados
        objetos_id = self.rastreador.rastreo(detecciones)

        for inf in objetos_id:
            x, y, w, h, id = inf
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, f'ID: {id}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame