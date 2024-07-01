class Product:
    def __init__(self, nombre, cantidad_vendidos, precio, stock, adicional):
        self.nombre = nombre
        self.cantidad_vendidos = cantidad_vendidos
        self.precio = precio 
        self.stock = stock
        self.adicional = adicional
        self.ventas = 0
    
    def show(self):
        print(
f"""
---> Nombre : {self.nombre}

---> Cantidad de ventas : {self.cantidad_vendidos}

---> Precio : {self.precio}

---> Cantidad restante : {self.stock}

---> Adicional : {self.adicional}

""")