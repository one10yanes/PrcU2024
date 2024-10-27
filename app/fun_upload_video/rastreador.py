class Rastreador:
    def __init__(self):
        self.centro_puntos = {}  # Diccionario para almacenar las posiciones de los centros de los vehículos
        self.id_count = 0         # Contador para asignar ID únicos a los vehículos

    def rastreo(self, objetos):
        objetos_id = []  # Lista para almacenar las detecciones con su ID

        # Iteramos sobre cada vehículo detectado
        for rect in objetos:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Verifica si el objeto ya ha sido rastreado
            mismo_objeto_detectado = False
            for id, pt in self.centro_puntos.items():
                dist = ((cx - pt[0]) ** 2 + (cy - pt[1]) ** 2) ** 0.5
                if dist < 25:
                    self.centro_puntos[id] = (cx, cy)
                    objetos_id.append([x, y, w, h, id])
                    mismo_objeto_detectado = True
                    break

            # Si es un nuevo objeto, asigna un nuevo ID
            if not mismo_objeto_detectado:
                self.centro_puntos[self.id_count] = (cx, cy)
                objetos_id.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Elimina los IDs que ya no se rastrean
        nuevos_centro_puntos = {}
        for obj_bb_id in objetos_id:
            _, _, _, _, object_id = obj_bb_id
            centro = self.centro_puntos[object_id]
            nuevos_centro_puntos[object_id] = centro

        self.centro_puntos = nuevos_centro_puntos.copy()
        return objetos_id