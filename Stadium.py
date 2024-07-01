class Stadium:
    def __init__(self, id, nombre, ciudad, capacidad, restaurantes):
        self.id = id
        self.nombre = nombre
        self.ciudad = ciudad
        self.capacidad = capacidad
        self.restaurantes = restaurantes
        self.entradas_vip = self.capacidad[1]
        self.entradas_generales = self.capacidad[0]
        self.visitantes = []
        self.asistencia = 0



    def show(self):
        total = self.entradas_generales + self.entradas_vip
        print(
            
f"""
                    ESTADIO : {self.nombre}

Ciudad : {self.ciudad}

Capacidad : {total}

""") 
        
        for restaurant in self.restaurantes:
            restaurant.show()