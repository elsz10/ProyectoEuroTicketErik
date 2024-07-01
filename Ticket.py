class Ticket:
    def __init__(self, id_cliente, id_partido, id_estadio):
        self.codigo = f"{str(id_cliente) + id_partido + id_estadio}"

    def show(self):
        print (
f"""
Código de entrada :  {self.codigo}
""")