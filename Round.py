class Round:
    def __init__(self, nombre, match_name, matches):
        self.nombre = nombre
        self.match_name = match_name
        self.matches = matches
    
    def show(self):
        print(
f"""
Torneo : {self.nombre}

Ronda : {self.match_name}

""")
        for match in self.matches:
            print(match)