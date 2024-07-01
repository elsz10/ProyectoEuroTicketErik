
class Restaurant:
    def __init__(self, nombre, productos, id_estadio):
        self.nombre = nombre
        self.productos = productos
        self.id_estadio = id_estadio

    def show(self):
        print(
f"""
                    RESTAURANT : {self.nombre}

Productos : 
""")
        for producto in self.productos:
            producto.show()