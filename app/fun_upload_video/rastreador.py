import math

class Rastreador:
    def __init__(self):
        self.centro_puntos = {}  # Diccionario para almacenar las posiciones de los centros de los vehículos
        self.id_count = 0         # Contador para asignar ID únicos a los vehículos

    def rastreo(self, objetos):
        objetos_id = []  # Lista para almacenar las detecciones con su ID

        # Iteramos sobre cada vehículo detectado
        for rect in objetos:
            x, y, w, h = rect
            cx = (x + x + w) // 2  # Calculamos el centro del vehículo (coordenada x)
            cy = (y + y + h) // 2  # Calculamos el centro del vehículo (coordenada y)
        
            objeto_detectado = False

            # Revisamos si el vehículo ya ha sido detectado anteriormente
            for id, pt in self.centro_puntos.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])  # Calculamos la distancia entre centros

                if dist < 25:  # Si la distancia es menor que 25 píxeles, consideramos que es el mismo vehículo
                    self.centro_puntos[id] = (cx, cy)  # Actualizamos la posición del centro del vehículo
                    objetos_id.append([x, y, w, h, id])  # Asignamos el mismo ID
                    objeto_detectado = True
                    break

            # Si el vehículo no ha sido detectado, le asignamos un nuevo ID
            if not objeto_detectado:
                self.centro_puntos[self.id_count] = (cx, cy)  # Guardamos el centro del nuevo vehículo
                objetos_id.append([x, y, w, h, self.id_count])  # Asignamos un nuevo ID
                self.id_count += 1  # Incrementamos el contador de IDs

        # Actualizamos el diccionario de puntos de centro solo con los vehículos detectados en el cuadro actual
        new_centro_puntos = {}
        for obj_bb_id in objetos_id:
            _, _, _, _, object_id = obj_bb_id
            center = self.centro_puntos[object_id]
            new_centro_puntos[object_id] = center

        # Reemplazamos el diccionario antiguo con el nuevo que contiene solo los vehículos activos
        self.centro_puntos = new_centro_puntos

        return objetos_id
