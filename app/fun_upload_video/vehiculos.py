import cv2
import numpy as np
import time
from rastreador import *  # Importa la clase Rastreador, que probablemente rastrea los objetos detectados.

seguimiento = Rastreador()  # Crea una instancia del objeto para hacer el seguimiento de los vehículos.

cap = cv2.VideoCapture('trafico.mp4')  # Carga el video desde el archivo 'trafico.mp4'.

# Inicializa un sustractor de fondo para detectar movimiento.
deteccion = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=100)

# Diccionarios para almacenar los tiempos de entrada y velocidad de los vehículos.
carI = {}
car0 = {}
prueba = {}

while True:
    # Lee un frame del video.
    ret, frame = cap.read()
    
    if not ret or frame is None:
        print("Error al leer el frame del video o fin del video.")
        break
    
    # Obtiene las dimensiones del frame (alto y ancho).
    height = frame.shape[0]
    width = frame.shape[1]
    
    # Crea una máscara vacía (negra) del tamaño del frame.
    mask = np.zeros((height, width), dtype=np.uint8)
  
    # Define una zona de interés (un polígono).
    pts = np.array([[[340,100], [540,100],  [850,300], [0,300] ]])
  
    # Rellena el área dentro del polígono en la máscara con blanco (255).
    cv2.fillPoly(mask, pts, 255)
    
    # Aplica la máscara a la imagen del frame.
    zona = cv2.bitwise_and(frame, frame, mask=mask)
      
    # Define tres áreas poligonales para detección y cálculo de velocidad.
    areag = [(340, 90), (540, 90), (850, 300), (0, 300)]  # Área general de interés.
    area1 = [(340, 90), (540, 90), (620,150), (225,150)]  # Área de detección inicial del vehículo.
    area2 = [(620,150), (225,150), (90, 240), (750, 240)]  # Área para medir la velocidad.
    area3 = [(90, 240), (750, 240), (990, 400), (-140, 400)]  # Área para mostrar la velocidad.

    # Dibuja los polígonos en el frame para visualización.
    #cv2.polylines(frame, [np.array(areag, np.int32)], True, (255,255,0), 2)
    #cv2.polylines(frame, [np.array(area1, np.int32)], True, (0,130,255), 2)
    #cv2.polylines(frame, [np.array(area2, np.int32)], True, (0,0,255), 2)
    #cv2.polylines(frame, [np.array(area3, np.int32)], True, (0,255,255), 2)    
    
    # Aplica el sustractor de fondo para obtener la máscara de movimiento.
    mascara = deteccion.apply(zona)
    
    # Suaviza la imagen binaria con un filtro gaussiano.
    filtro = cv2.GaussianBlur(mascara, (1, 1), 0)  # El tamaño del kernel es (1,1), pero puede ajustarse a (3,3) o (5,5) para más suavidad.

    # Aplica un umbral para convertir la imagen a blanco y negro (binaria).
    _, umbral = cv2.threshold(filtro, 50, 255, cv2.THRESH_BINARY)  # Los valores de umbral recomendados están entre 40 y 60 para videos de tráfico.

    # Dilata los píxeles blancos para hacer las áreas más visibles.
    dila = cv2.dilate(umbral, np.ones((9, 9)))  # La dilatación usa un kernel de 9x9. Valores mínimos de (3,3) y máximos de (15,15).

    # Crea un kernel estructural para cerrar pequeños agujeros en las detecciones.
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))  # Puede variar entre (3,3) y (5,5) dependiendo del ruido en la imagen.
    
    # Aplica la operación de cierre para eliminar agujeros pequeños.
    cerrar = cv2.morphologyEx(dila, cv2.MORPH_CLOSE, kernel)

    # Encuentra los contornos en la imagen binaria.
    contornos, _ = cv2.findContours(cerrar, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    detecciones = []  # Lista para almacenar las detecciones.

    # Filtra los contornos por área para evitar detecciones falsas.
    for cont in contornos:
        area = cv2.contourArea(cont)
        if area > 2000:  # Filtra objetos muy pequeños (recomendado entre 1500 y 2000 para tráfico).
            x, y, ancho, alto = cv2.boundingRect(cont)  # Obtiene las coordenadas del rectángulo envolvente.
            detecciones.append([x, y, ancho, alto])  # Almacena la detección.

    # Realiza el seguimiento de las detecciones usando la clase Rastreador.
    info_id = seguimiento.rastreo(detecciones)

    for inf in info_id:
        x, y, w, h, id = inf  # Descompone la información de detección.
        
        # Dibuja un rectángulo alrededor del vehículo detectado.
        cv2.rectangle(frame, (x, y - 10), (x + ancho, y + alto), (0, 0, 255), 2)
        
        # Calcula el centroide del vehículo.
        cx = int(x + ancho / 2)
        cy = int(y + alto / 2)

        # Verifica si el centroide está en el área de medición de velocidad (area2).
        a2 = cv2.pointPolygonTest(np.array(area2, np.int32), (cx, cy), False)

        if a2 >= 0:  # Si está en el área, guarda el tiempo de entrada.
            carI[id] = time.process_time()

        if id in carI:  # Si el vehículo ya tiene un tiempo registrado:
            cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)  # Dibuja un círculo en el centro del vehículo.
            
            # Verifica si el vehículo está en el área de visualización de velocidad (area3).
            a3 = cv2.pointPolygonTest(np.array(area3, np.int32), (cx, cy), False)

            if a3 >= 0:  # Si está en el área 3:
                tiempo = time.process_time() - carI[id]  # Calcula el tiempo que ha pasado desde que entró en el área 2.
                
                # Ajusta el tiempo para hacer correcciones.
                if tiempo % 1 == 0:
                    tiempo = tiempo + 0.323
                if tiempo % 1 != 0:
                    tiempo = tiempo + 1.016
                
                # Si es la primera vez que se detecta en el área 3, almacena el tiempo.
                if id not in car0:
                    car0[id] = tiempo

                if id in car0:  # Calcula la velocidad.
                   tiempo = car0[id]
                   vel = 20 / car0[id]  # La distancia es 20 metros APROXIMADOS.
                   vel = vel * 3.6  # Convierte la velocidad a km/h.
                
                # Dibuja un rectángulo y muestra la velocidad del vehículo.
                cv2.rectangle(frame, (x, y - 10), (x + 30, y + 10), (0, 255, 0), -1)
                cv2.putText(frame, str(int(vel)) + " km/h", (x, y - 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Muestra el ID del vehículo.
        cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)        

    # Muestra los frames procesados en tiempo real.
    cv2.imshow('Carretera', frame)
    cv2.imshow('Mascara', filtro)

    # Espera a que el usuario presione la tecla 'ESC' para salir.
    key = cv2.waitKey(5) 
    if key == 27:
        break

# Libera el video y cierra todas las ventanas.
cap.release()
cv2.destroyAllWindows()
