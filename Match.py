from Team import Team

class Match:
    def __init__(self, id, numero, local, visitante, fecha, grupo, id_estadio, registro_entradas):
        self.id = id
        self.numero = numero
        self.local = local
        self.visitante = visitante
        self.fecha = fecha
        self.grupo = grupo
        self.id_estadio = id_estadio
        self.registro_entradas = registro_entradas
    
    def show(self):
        print(
f"""
ID : {self.id}

Numero : {self.numero}

Local : {self.local.country}

Visitante : {self.visitante.country}

Fecha : {self.fecha}

Grupo : {self.grupo}

ID estadio : {self.id_estadio}

""")
