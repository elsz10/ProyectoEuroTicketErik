from Match import Match
from Team import Team
from Round import Round
from Stadium import Stadium
from Restaurant import Restaurant
from Product import Product
from Client import Client
from Ticket import Ticket
from Vampiro import Vampiro
from Grafico import Grafico
import pickle
import requests
import msvcrt

class App:
    def __init__(self):
        self.lista_entradas = []
        self.lista_estadios = []
        self.lista_equipos = []
        self.lista_restaurantes = []
        self.lista_productos = []
        self.lista_partidos = []
        self.lista_rondas = []
        self.lista_clientes = []
        self.lista_tickets = []
        self.logged_cliente = None

    def load_data(self):
        self.load_matches()
        self.load_teams()
        self.load_rounds()        
        self.load_stadiums()


    def load_matches(self):
        res = requests.request("GET", "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json").json()        

        for match in res:

            team_home = Team(match["home"]["id"], match["home"]["code"], match["home"]["name"], match["home"]["group"])
            
            team_away = Team(match["away"]["id"], match["away"]["code"], match["away"]["name"], match["away"]["group"])
                
            newMatch = Match(match["id"], match["number"], team_home, team_away, match["date"], match["group"], match["stadium_id"], [])
            self.lista_partidos.append(newMatch)

    def load_teams(self):
        res = requests.request("GET", "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json").json()

        for team in res:
            newTeam = Team(team["id"], team["code"], team["name"], team["group"])
            self.lista_equipos.append(newTeam)

    def load_rounds(self):
        res = requests.request("GET", "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/rounds.json").json()
        name = res["name"]
        matchesList = []
        for API_rounds in res["rounds"]: 
            match_name = API_rounds["name"]
            for i in range(len(API_rounds["matches"])):
                round = API_rounds["matches"][i] 
                matchesList.append(round)         

            newRound = Round(name, match_name, matchesList)

        self.lista_rondas.append(newRound)

    def load_stadiums(self):
        res = requests.request("GET", "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()
        for stadiums in res:
            restaurants_list = []
            capacidad = []
            productos_l = []
            for capacity in stadiums["capacity"]:
                capacidad.append(capacity)
            
            for restaurant in stadiums["restaurants"]:

                for productos in restaurant["products"]:
                    newProduct = Product(productos["name"], productos["quantity"], productos["price"], productos["stock"], productos["adicional"])
                    productos_l.append(newProduct)
                    self.lista_productos.append(newProduct)

                newRest = Restaurant(restaurant["name"], productos_l, stadiums["id"])
                restaurants_list.append(newRest)
                

            newStadium = Stadium(stadiums["id"], stadiums["name"], stadiums["city"], capacidad, restaurants_list)
            self.lista_estadios.append(newStadium)

        
        
    def start(self, bool):
        if bool:
            self.load_data()

        while True:
            try:
                seleccion = int(input(

"""
        Bienvenido a EuroTickets 2024
Para ingresar seleccione una opción:
    1- Busqueda de partidos
    2- Venta de entradas
    3- Ingresar a estadio
    4- Estadísticas
    5- Guardar data
    6- Salir

>>
"""))
                if seleccion < 1 or seleccion > 6:
                    raise ValueError
                
                if seleccion == 1:
                    self.menu_busqueda_partidos()
                
                if seleccion == 2:
                    self.vender_entrada()
                
                if seleccion == 3:
                    self.entrar_estadio()

                if seleccion == 4:
                    self.menu_estadisticas()
                
                if seleccion == 5:
                    self.save_object("ClientsList", self.lista_clientes)
                    self.save_object("PartidosList", self.lista_partidos)
                    self.save_object("RestaurantesList", self.lista_restaurantes)
                    self.save_object("ProductsList", self.lista_productos)
                    self.save_object("EntradasList", self.lista_entradas)
                    self.save_object("RoundsList", self.lista_rondas)
                    self.save_object("TicketsList", self.lista_tickets)
                    self.save_object("StadiumsList", self.lista_estadios)

                
                if seleccion == 6:
                    print("Gracias por usar EuroTickets, hasta pronto!!")
                    break

            
            except:
                self.mostrar_mensaje("Dato inválido")
    
    def save_object(self, nombre, listas):
        with open(f"{nombre}.pickle", "wb+") as f:
            pickle.dump(listas, f)
    
    def menu_estadio(self):
        while True:
            try:
                estadio_temp = self.encuentra_estadio()
                seleccion = int(input(
f"""
                    Bienvenido al estadio {estadio_temp.nombre}

Para continuar seleccion una opción:
    1- Buscar partidos
    2- Entrar al área VIP
    3- Salir del estadio

>>
"""))
                if seleccion < 1 or seleccion > 3:
                    raise ValueError

                if seleccion == 1:
                    self.menu_busqueda_partidos()
                
                if seleccion == 2:
                    self.menu_restaurantes(estadio_temp)
                
                if seleccion == 3:
                    print(
f"""
Gracias por visitar el estadio {estadio_temp.nombre}

Hasta pronto!!
""")
                    self.start(False)
            except:
                self.mostrar_mensaje("Dato inválido")
    
    def entrar_estadio(self):
         while True:
            try:
                print(
"""
Para entrar al estadio se debe verificar si la entrada es auténtica

Ingrese los datos solicitados
""")
                cedula = int(input("Ingrese el número de cédula del cliente : "))
                self.logged_cliente = None
                for cliente in self.lista_clientes:
                    if cliente.cedula == cedula:
                        self.logged_cliente = cliente
                
                if self.logged_cliente == None:
                    raise ValueError
                    
                if self.validar_entrada():
                    self.menu_estadio()

                else:
                    self.mostrar_mensaje("El cliente no posee una entrada al partido") 
                    break             

            except:
                self.mostrar_mensaje("Dato inválido")
                break
    
                 
    def validar_entrada(self):
        temp = False
        for match in self.lista_partidos:
            for ticket in match.registro_entradas:
                if ticket == self.logged_cliente.codigo_entrada: 
                    temp = True
        
        return temp
                                        
    
    def menu_busqueda_partidos(self):
        while True:
            try:
                seleccion = int(input(
"""
Indique el filtro de búsqueda:
    1- Busqueda por país
    2- Busqueda por fecha
    3- Busqueda por estadio
    4- Atrás

>>
"""))
                if seleccion == 1:
                    self.busqueda_pais()
                
                if seleccion == 2:
                    self.busqueda_fecha()
                
                if seleccion == 3:
                    self.busqueda_estadio()
                
                if seleccion == 4:
                    break
            
            except:
                self.mostrar_mensaje("Dato inválido")
    
    def busqueda_pais(self):
        temp = None
        pais = input("Ingrese el país que desea buscar: ").lower()
        for ind in range(len(self.lista_partidos)):
            if self.lista_partidos[ind].local.country.lower() == pais or self.lista_partidos[ind].visitante.country.lower() == pais :
                temp = self.lista_partidos[ind]
                temp.show() 
        
        self.mostrar_mensaje("")
        
        if temp == None:
            self.mostrar_mensaje("No hay partidos que coincidan con la búsqueda")

    def busqueda_fecha(self):
        temp = None
        fecha = input("Ingrese la fecha que desea buscar: ")
        for ind in range(len(self.lista_partidos)):
            if self.lista_partidos[ind].fecha == fecha:
                temp = self.lista_partidos[ind]
                temp.show() 
        
        self.mostrar_mensaje("")
        
        if temp == None:
            self.mostrar_mensaje("No hay partidos que coincidan con la búsqueda")
    
    def busqueda_estadio(self):
        temp = None
        estadio = input("Ingrese el estadio que desea buscar: ").lower()
        for ind in range(len(self.lista_estadios)):
            if self.lista_estadios[ind].nombre.lower() == estadio:
                id_stadium = self.lista_estadios[ind].id
                for i in range(len(self.lista_partidos)):
                    if self.lista_partidos[i].id_estadio == id_stadium:
                        temp = self.lista_partidos[i]
                        temp.show() 
        
        self.mostrar_mensaje("")
        
        if temp == None:
            self.mostrar_mensaje("No hay partidos que coincidan con la búsqueda")
    
    def vender_entrada(self):
        while True:
            print(
    """
                        Venta de entradas :

    Para continuar ingrese los datos solicitados del cliente:
    """)
            try:
                precio_entrada = 0
                nombre = input("Nombre del cliente : ").lower()
                cedula = int(input("Cédula del cliente : "))
                edad = int(input("Edad del cliente : "))
                if edad < 15 or edad > 90:
                    raise ValueError
                
                partido_ver = self.muestra_partidos()
                pregunta = int(input(
    """
    Tipo de entrada:
        1- General --> 35$
        2-   VIP   --> 75$

    """))
                if pregunta == 1:
                    tipo_entrada = "general"
                    for stadium in self.lista_estadios:
                        if stadium.id == partido_ver.id_estadio:
                            stadium.entradas_generales -= 1
                            precio_entrada = 35.00
                
                if pregunta == 2:
                    tipo_entrada = "vip"
                    for stadium in self.lista_estadios:
                        if stadium.id == partido_ver.id_estadio:
                            stadium.entradas_vip -= 1
                            precio_entrada = 75.00
                
                if pregunta < 1 or pregunta > 2:
                    raise ValueError
                
                confirmacion = int(input(
    """
    ¿Desea confirmar el pago?
        1- Si
        2- No

    >>
    """))
                if confirmacion < 1 or confirmacion > 2:
                    raise ValueError
                if confirmacion == 1:

                    newTicket = Ticket(cedula, partido_ver.id, partido_ver.id_estadio)
                    newClient = Client(nombre, cedula, edad, partido_ver.numero , tipo_entrada, "", [], newTicket.codigo)

                    for stadium in self.lista_estadios:
                        if stadium.id == partido_ver.id_estadio:
                            stadium.visitantes.append(newClient.cedula)
                            stadium.asistencia += 1

                    self.lista_clientes.append(newClient)
                    self.lista_tickets.append(newTicket)
                    partido_ver.registro_entradas.append(newTicket.codigo)
                    self.factura_entrada(precio_entrada, newClient)
                    self.mostrar_mensaje("Pago de entrada realizado exitosamente!!")
                    break
                
                if confirmacion == 2:
                    break
            
            except:
                self.mostrar_mensaje("Dato inválido")
    
    def factura_entrada(self, precio_entrada, cliente):
        subtotal = precio_entrada
        iva = subtotal * 0.16
        total = subtotal + iva
        descuento = "0%"
        vamp = Vampiro()
        if vamp.esVampiro(cliente.cedula):
            descuento = "50%"
            total *= 0.50
        
        cliente.gastos += total
        
        print(
f"""
                    Factura:

Nombre del cliente : {cliente.nombre}

Subtotal : {subtotal}

IVA : {iva}

Descuento : {descuento}

Total : {total}


""")




    
    def muestra_partidos(self):
        for partido in self.lista_partidos:
            partido.show()
        while True:        
            try:
                temp = 0
                seleccion = int(input("Ingrese el número del partido que el cliente desea ver : "))
                for i in range(len(self.lista_partidos)):
                    if self.lista_partidos[i].numero == seleccion:
                        return self.lista_partidos[i]
                    
                    else:
                        temp += 1
                
                if temp == (len(self.lista_partidos) - 1):
                    raise ValueError            
            except:
                self.mostrar_mensaje("Partido no encontrado")
    

    def autenticacion_vip(self, estadio):
        while True:
            try:
                vip = False
                confirmacion = False
                verificado = int(input("Ingrese el número de cédula del cliente : "))
                for id_cliente in estadio.visitantes:
                    if id_cliente == verificado:
                        confirmacion = True

                for i in range(len(self.lista_clientes)):
                    if self.lista_clientes[i].cedula == verificado and self.lista_clientes[i].tipo_entrada == "vip" and confirmacion == True:
                        self.logged_cliente = self.lista_clientes[i]
                        vip = True
                        break                    
                    
                break

            except:
                self.mostrar_mensaje("Dato inválido")

        return vip
    
    def encuentra_estadio(self):
        for partido in self.lista_partidos:
            if partido.numero == self.logged_cliente.partido:
                id_estadio = partido.id_estadio
                break
        
        for estadio in self.lista_estadios:
            if estadio.id == id_estadio:
                return estadio

                                 

    def menu_restaurantes(self, estadio):
        if self.autenticacion_vip(estadio):
            while True:
                try:
                    seleccion = int(input(
f"""
                    Bienvenido al area VIP del estadio {estadio.nombre}

Para continuar seleccione una opción:
    1- Buscar producto
    2- Comprar producto
    3- Atrás

>>
"""))
                    if seleccion < 1 or seleccion > 3:
                        raise ValueError
                    
                    if seleccion == 1:
                        self.menu_busqueda_productos()
                    
                    if seleccion == 2:
                        self.menu_producto(estadio)
                    
                    if seleccion == 3:
                        break
                
                except:
                    self.mostrar_mensaje("Dato inválido")
                    
                
        else:
            self.mostrar_mensaje("El cliente no posee una entrada VIP")
            return
    
    def menu_busqueda_productos(self):
        while True:
            try:
                seleccion = int(input(
"""
Seleccione el tipo de búsqueda que desea realizar:
    1- Búsqueda por nombre
    2- Búsqueda por tipo
    3- Búsqueda por precio
    4- Atrás
"""))
                if seleccion < 1 or seleccion > 4:
                    raise ValueError
                
                if seleccion == 1:
                    self.busqueda_producto_nombre()
                
                if seleccion == 2:
                    self.busqueda_producto_tipo()
                
                if seleccion == 3:
                    self.busqueda_producto_precio()
                
                if seleccion == 4:
                    break
            except:
                self.mostrar_mensaje("Dato inválido")
    

    def busqueda_producto_nombre(self):
        temp = None
        nombre = input("Ingrese el nombre del producto que desea buscar: ").lower()
        for ind in range(len(self.lista_productos)):
            if self.lista_productos[ind].nombre.lower() == nombre:
                temp = self.lista_productos[ind]
                temp.show() 
        
        self.mostrar_mensaje("")
        
        if temp == None:
            self.mostrar_mensaje("No hay productos que coincidan con la búsqueda")
    
    def busqueda_producto_tipo(self):
        temp = None
        tipo = input("Ingrese el tipo del producto que desea buscar: ").lower()
        for ind in range(len(self.lista_productos)):
            if self.lista_productos[ind].adicional.lower() == tipo:
                temp = self.lista_productos[ind]
                temp.show() 
        
        self.mostrar_mensaje("")
        
        if temp == None:
            self.mostrar_mensaje("No hay productos que coincidan con la búsqueda")
    
    def busqueda_producto_precio(self):
        temp = None
        precio = input("Ingrese el precio del producto que desea buscar: ").lower()
        for ind in range(len(self.lista_productos)):
            if self.lista_productos[ind].precio == precio:
                temp = self.lista_productos[ind]
                temp.show() 
        
        self.mostrar_mensaje("")
        
        if temp == None:
            self.mostrar_mensaje("No hay productos que coincidan con la búsqueda")

    
    def menu_producto(self, estadio):
        carrito = []
        temp_estadio = estadio
        while True:
            try:
                seleccion = int(input(
"""
¿Que desea comprar el cliente?
    1- Bebida
    2- Alimento
    3- Salir

>>
"""))
                if seleccion < 1 or seleccion > 3:
                    raise ValueError

                if seleccion == 1:
                    self.comprar_bebida(temp_estadio, carrito)
                
                if seleccion == 2:
                    self.comprar_alimento(temp_estadio, carrito)
                
                if seleccion == 3:
                    break
                          
            except :
                self.mostrar_mensaje("Dato inválido")
    
    def comprar_alimento(self, estadio, carrito):
        lista_productos = []
        for i in range(len(estadio.restaurantes)):
            for producto in estadio.restaurantes[i].productos:
                if producto.adicional == "package" or producto.adicional == "plate":
                    producto.show()
                    lista_productos.append(producto)
            
        while True:
            try:
                eleccion = input("Ingrese el nombre del alimento que el cliente desea comprar : ").lower()

                for producto in lista_productos:
                    if producto.nombre.lower() == eleccion:
                        carrito.append(producto)   
                        compra = int(input(
"""
¿El cliente desea comprar otro producto?
1- Si
2- No

"""))
                        if compra == 1:
                            break

                        if compra == 2:
                            confirmacion = int(input(
"""
Confirmar pago :
1- Si
2- No

"""))
                            if confirmacion == 1:
                                self.mostrar_factura(carrito)
                                self.mostrar_mensaje("")
                                break

                            if confirmacion == 2:
                                break

                            if confirmacion < 1 or confirmacion > 2:
                                raise ValueError


                
                break
            
            except:
                self.mostrar_mensaje("Dato inválido")

    
    def comprar_bebida(self, estadio, carrito):
        
        lista_productos = []
        for i in range(len(estadio.restaurantes)):
            for producto in estadio.restaurantes[i].productos:
                if producto.adicional == "alcoholic" or producto.adicional == "non-alcoholic":
                    producto.show()
                    lista_productos.append(producto)
            
        while True:
            try:
                eleccion = input("Ingrese el nombre de la bebida que el cliente desea comprar : ").lower()

                for producto in lista_productos:
                    if producto.nombre.lower() == eleccion:
                        if producto.adicional == "alcoholic" and self.logged_cliente.edad < 18:
                            print("Los clientes menores de 18 años de edad no pueden adquirir bebidas alcohólicas")
                            break
                        else: 
                            carrito.append(producto)   
                            compra = int(input(
"""
¿El cliente desea comprar otro producto?
    1- Si
    2- No

"""))
                            if compra == 1:
                                break

                            if compra == 2:
                                confirmacion = int(input(
"""
Confirmar pago :
1- Si
2- No

"""))
                                if confirmacion == 1:
                                    self.mostrar_factura(carrito)
                                    self.mostrar_mensaje("")
                                    break

                                if confirmacion == 2:
                                    break

                                if confirmacion < 1 or confirmacion > 2:
                                    raise ValueError


                
                break
            
            except:
                self.mostrar_mensaje("Dato inválido")
    
    def mostrar_factura(self, carrito):
        descuento = "0%"
        total = 0
        subtotal = 0
        iva = 0
        for producto in carrito:
            self.logged_cliente.productos_consumo.append(producto)
            producto.stock -= 1
            producto.ventas += 1
            subtotal += float(producto.precio)
            print(f"Producto : {producto.nombre}")

        iva = subtotal * 0.16
        total = subtotal + iva

        

        if self.evaluar_nro_perfecto(self.logged_cliente.cedula):
            descuento = "15%"
            total *= 0.15

        for cliente in self.lista_clientes:
            if cliente.cedula == self.logged_cliente.cedula:
                cliente.gastos += total

        print(
f"""

Subtotal: {float(subtotal)}

Descuento : {descuento}

IVA : {iva}

Total a pagar : {float(total)}

""")
    

    def evaluar_nro_perfecto(self, numero):
        i = 2
        suma = 0
        while i <= numero:
            if numero % i == 0:
                suma += numero//i
            i += 1

        if suma == numero:
            return True
        else:
            return False 
        

    def order_lista_ventas(self, lista):
       # Selection Sort
       n = len(lista)
       for i in range(n):
           min_idx = i
           for j in range (i + 1, n):
               if lista[min_idx].ventas > lista[j].ventas:
                   min_idx = j
           lista[i], lista[min_idx] = lista[min_idx], lista[i]
       return lista
    
    def order_lista_clientes(self, lista):
       # Selection Sort
       n = len(lista)
       for i in range(n):
           min_idx = i
           for j in range (i + 1, n):
               if lista[min_idx].cantidad_compras > lista[j].cantidad_compras:
                   min_idx = j
           lista[i], lista[min_idx] = lista[min_idx], lista[i]
       return lista

    def top3_productos(self):
        names_list = []
        cant_list = []
        copia_lista_productos = self.lista_productos
        copia_lista_productos = self.order_lista_ventas(copia_lista_productos)
        longitud = len(copia_lista_productos)
        top = 0
        for i in range(longitud):
            top += 1
            if i >= 3:
                break
            names_list.append(copia_lista_productos[longitud-i-1].nombre)
            cant_list.append(copia_lista_productos[longitud-i-1].ventas)
            print(
f"""
                            TOP {top}
    -Producto : {copia_lista_productos[longitud-i-1].nombre}
    -Ventas  :  {copia_lista_productos[longitud-i-1].ventas}

""")
        self.menu_grafic_view(names_list, cant_list)
        self.mostrar_mensaje("")
    
    def top3_compras_clientes(self):
        if len(self.lista_clientes) == 0:
            self.mostrar_mensaje("No hay clientes registrados en el sistema")
            return
        names_list = []
        cant_list = []
        copia_lista_clientes = self.lista_clientes
        copia_lista_clientes = self.order_lista_clientes(copia_lista_clientes)
        longitud = len(copia_lista_clientes)
        top = 0
        for i in range(longitud):
            top += 1
            if i >= 3:
                break
            names_list.append(copia_lista_clientes[longitud-i-1].nombre)
            cant_list.append(len(copia_lista_clientes[longitud-i-1].productos_consumo))
            print(
f"""
                            TOP {top}
    -Cliente : {copia_lista_clientes[longitud-i-1].nombre}
    -Cantidad de compras  :  {len(copia_lista_clientes[longitud-i-1].cantidad_compras)}

""")
        self.menu_grafic_view(names_list, cant_list)
        self.mostrar_mensaje("")
    

    def order_lista_estadios(self, lista):
        n = len(lista)
        for i in range(n):
            min_idx = i
            for j in range (i + 1, n):
                if lista[min_idx].asistencia > lista[j].asistencia:
                    min_idx = j
            lista[i], lista[min_idx] = lista[min_idx], lista[i]
        return lista



    def menu_estadisticas(self):
        while True:
            try:
                seleccion = int(input(
"""
Para visualizar las estadísticas de la Eurocopa seleccione una opción:
    1- Promedios de gasto
    2- Asistencias a partidos
    3- Partido con mayor venta de entradas
    4- Top 3 productos más vendidos
    5- Top 3 clientes con más compras
    6- Salir

>>
"""))
                if seleccion < 1 or seleccion > 6:
                    raise ValueError
                
                if seleccion == 1:
                    self.promedio_gastos()
                
                if seleccion == 2:
                    self.tabla_asistencias()
                
                if seleccion == 3:
                    self.mayor_venta()
                
                if seleccion == 4:
                    self.top3_productos()
                
                if seleccion == 5:
                    self.top3_compras_clientes()
                
                if seleccion == 6:
                    break
            
            except:
                self.mostrar_mensaje("Dato inválido")

    def tabla_asistencias(self):
        names_list = []
        cant_list = []
        copia_lista_partidos = self.lista_partidos
        copia_lista_partidos = self.order_lista_partidos(copia_lista_partidos)
        longitud = len(copia_lista_partidos)
        top = 0
        for i in range(longitud):
            top += 1
            names_list.append(copia_lista_partidos[longitud-i-1].numero)
            cant_list.append(len(copia_lista_partidos[longitud-i-1].registro_entradas))

            for estadio in self.lista_estadios:
                if estadio.id == copia_lista_partidos[longitud-i-1].id_estadio:
                    nombre_estadio = estadio.nombre
            print(
f"""
                            TOP {top}

    -Numero : {copia_lista_partidos[longitud-i-1].numero}

    -Local: {copia_lista_partidos[longitud-i-1].local.country}

    -Visitante : {copia_lista_partidos[longitud-i-1].visitante.country}

    -Estadio : {nombre_estadio}

    -Entradas Vendidas : {len(copia_lista_partidos[longitud-i-1].registro_entradas)}

""")
        self.menu_grafic_view(names_list, cant_list)
        self.mostrar_mensaje("")


    def promedio_gastos(self):
        cuentas_generales = 0
        clientes_vip = 0
        for cliente in self.lista_clientes:
            if cliente.tipo_entrada == "vip":
                cuentas_generales += cliente.gastos
                clientes_vip += 1

        promedio_gastos = cuentas_generales / clientes_vip
        print(
f"""
El promedio de gastos de un cliente VIP es de : {promedio_gastos}$

""")
        self.mostrar_mensaje("")

    def mayor_venta(self):
        names_list = []
        cant_list = []
        copia_lista_partidos = self.lista_partidos
        copia_lista_partidos = self.order_lista_partidos(copia_lista_partidos)
        longitud = len(copia_lista_partidos)
        top = 0
        for i in range(longitud):
            top += 1
            if i >= 1:
                break
            names_list.append(copia_lista_partidos[longitud-i-1].numero)
            cant_list.append(copia_lista_partidos[longitud-i-1].registro_entradas)
            print(
f"""
                            TOP {top}
    -Numero : {copia_lista_partidos[longitud-i-1].numero}

    -Local: {copia_lista_partidos[longitud-i-1].local.country}

    -Visitante : {copia_lista_partidos[longitud-i-1].visitante.country}

    -Entradas Vendidas : {len(copia_lista_partidos[longitud-i-1].registro_entradas)}

""")
        self.mostrar_mensaje("")
     
    
    def order_lista_partidos(self, lista):
        n = len(lista)
        for i in range(n):
            min_idx = i
            for j in range (i + 1, n):
                if len(lista[min_idx].registro_entradas) > len(lista[j].registro_entradas):
                    min_idx = j
            lista[i], lista[min_idx] = lista[min_idx], lista[i]
        return lista

    def menu_grafic_view(self, names, views): 
        #Menú para confirmar si el usuario desea ver el gráfico correspondiente al top
        while True:
            try:
                seleccion = int(input(
"""
¿Desea ver el gráfico de este top?
    1-Si
    2-No
"""))
                if seleccion < 1 or seleccion > 2:
                    raise ValueError

                if seleccion == 1:
                    grafic = Grafico()
                    grafic.show_grafic(names, views)
                    break
                
                if seleccion == 2:
                    break
            except:
                self.mostrar_mensaje("Dato inválido")
    
        
      
        
    def mostrar_mensaje(self, mensaje):
        # Método para mostrar un mensaje el cual se recibe por parámetro
        # Luego se le pide al usuario que presione cualquier tecla para continuar
        print(mensaje)
        print("Presione cualquier tecla para continuar...")
        msvcrt.getch()
    

        
    