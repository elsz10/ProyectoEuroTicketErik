class Team:
    def __init__ (self, id,  FIFAcode, country, group):
        self.id = id
        self.country = country
        self.FIFAcode = FIFAcode
        self.group = group
    
    def show(self):
        print(

f"""
ID : {self.id}

País : {self.country}

Código FIFA : {self.FIFAcode}

Grupo : {self.group}

""")
    