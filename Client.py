class Client:
    def __init__(self, nombre, cedula, edad, partido, tipo_entrada, asiento, productos_consumo, codigo_entrada):
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad
        self.partido = partido
        self.tipo_entrada = tipo_entrada
        self.asiento = asiento
        self.productos_consumo = productos_consumo
        self.codigo_entrada = codigo_entrada
        self.cantidad_compras = len(self.productos_consumo)
        self.gastos = 0

    

    def show(self):
        print(
f"""
Nombre: {self.nombre}

Cédula: {self.id}

Edad: {self.edad}

Partido a ver: {self.partido}

Tipo de entrada: {self.tipo_entrada}

Asiento asignado : {self.asiento}

Código de entrada : {self.codigo_entrada}


""")