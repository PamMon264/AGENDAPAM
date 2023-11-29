import pymongo
from datetime import datetime

print("\nBIENVENID@ A LA AGENDA DE CONTACTOS DE PAM")

class Persona:
    def __init__(self, nombre, apellido, fecha_nacimiento):
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'fecha_nacimiento': self.fecha_nacimiento.strftime("%Y-%m-%d")  # Convertir a formato de cadena
        }

class Direccion:
    def __init__(self, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia):
        self.calle = calle
        self.ciudad = ciudad
        self.codigo_postal = codigo_postal
        self.numero_exterior = numero_exterior
        self.numero_interior = numero_interior
        self.colonia = colonia

    def to_dict(self):
        return {
            'calle': self.calle,
            'ciudad': self.ciudad,
            'codigo_postal': self.codigo_postal,
            'numero_exterior': self.numero_exterior,
            'numero_interior': self.numero_interior,
            'colonia': self.colonia
        }

class Telefono:
    def __init__(self, numero):
        self.numero = numero

    def to_dict(self):
        return {'numero': self.numero}

class CorreoElectronico:
    def __init__(self, email, pagina_web):
        self.email = email
        self.pagina_web = pagina_web

    def to_dict(self):
        return {'email': self.email, 'pagina_web': self.pagina_web}

class Contacto(Persona, Direccion, Telefono, CorreoElectronico):
    def __init__(self, nombre, apellido, fecha_nacimiento, calle, ciudad, codigo_postal, numero_exterior, 
                 numero_interior, colonia, numero, email, pagina_web):
        
        fecha_nacimiento_dt = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
        
        Persona.__init__(self, nombre, apellido, fecha_nacimiento_dt)
        Direccion.__init__(self, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia)
        Telefono.__init__(self, numero)
        CorreoElectronico.__init__(self, email, pagina_web)

    def to_dict(self):
        contacto_dict = {}
        contacto_dict.update(Persona.to_dict(self))
        contacto_dict.update(Direccion.to_dict(self))
        contacto_dict.update(Telefono.to_dict(self))
        contacto_dict.update(CorreoElectronico.to_dict(self))
        return contacto_dict

class Agenda:
    def __init__(self):
       
        connection_string = "mongodb+srv://agendapx:1234.@agenda.snyekgy.mongodb.net/"
        self.cliente = pymongo.MongoClient(connection_string)
        self.db = self.cliente["Agenda"]
        self.collection = self.db["contactos"]
    
    def buscar_contacto(self):
        print("\nBuscar contacto por:")
        print("1. Nombre")
        print("2. Número de Teléfono")
        opcion_busqueda = input("Seleccione la opción de búsqueda (1-2): ")

        if opcion_busqueda == "1":
            nombre_busqueda = input("Ingrese el nombre del contacto a buscar: ")
            contactos = self.collection.find({'nombre': nombre_busqueda}).sort('nombre')
        elif opcion_busqueda == "2":
            numero_busqueda = input("Ingrese el número de teléfono del contacto a buscar: ")
            contactos = self.collection.find({'numero': numero_busqueda})
        else:
            print("Opción no válida.")
            return

        contactos_lista = list(contactos)

        if not contactos_lista:
            print("No se encontraron contactos.")
        else:
            print("\nResultados de la búsqueda:")
            for i, contacto in enumerate(contactos_lista):
                print("\nContacto {}:".format(i + 1))
                for key, value in contacto.items():
                    print(f"{key.capitalize()}: {value}")


    def agregar_contacto(self, contacto):
        self.collection.insert_one(contacto.to_dict())
        print("Contacto agregado exitosamente.")

    def visualizar_agenda(self):
        
        contactos = self.collection.find().sort('nombre')

      
        contactos_lista = list(contactos)

        if len(contactos_lista) == 0:
            print("La agenda está vacía.")
        else:
            print("\nAgenda:")
            print("{:<5} {:<15} {:<15} {:<15} {:<20} {:<15}".format(
                "ID", "Nombre", "Apellido", "Fecha Nac.", "Teléfono", "Correo Electrónico"))
            print("-" * 85)

            for i, contacto in enumerate(contactos_lista):
                print("{:<5} {:<15} {:<15} {:<15} {:<20} {:<15}".format(
                    str(i + 1),
                    contacto['nombre'],
                    contacto['apellido'],
                    contacto['fecha_nacimiento'],
                    contacto['numero'],
                    contacto['email']
                ))
            print("-" * 85)

    def modificar_contacto(self):
        # Muestra la lista de contactos
        self.visualizar_agenda()

        # Solicitar al usuario el número de teléfono del contacto a modificar
        numero_telefono = input("Ingrese el número de teléfono del contacto a modificar: ")

        # Encuentra el contacto en la base de datos por el número de teléfono
        contacto = self.collection.find_one({'numero': numero_telefono})

        if contacto:
            print(f"\nModificando contacto con el número de teléfono: {numero_telefono}")
            print("1. Modificar Nombre")
            print("2. Modificar Apellido")
            print("3. Modificar Fecha de Nacimiento")
            print("4. Modificar Número de Teléfono")
            print("5. Modificar Correo Electrónico")
            opcion = input("Seleccione el campo que desea modificar (1-5): ")

            if opcion == "1":
                nuevo_nombre = input("Nuevo nombre: ")
                self.collection.update_one({'numero': numero_telefono}, {'$set': {'nombre': nuevo_nombre}})
                print("Nombre modificado exitosamente.")
            elif opcion == "2":
                nuevo_apellido = input("Nuevo apellido: ")
                self.collection.update_one({'numero': numero_telefono}, {'$set': {'apellido': nuevo_apellido}})
                print("Apellido modificado exitosamente.")
            elif opcion == "3":
                nuevo_fecha_nacimiento = input("Nueva fecha de nacimiento (YYYY-MM-DD): ")
                nuevo_fecha_nacimiento_dt = datetime.strptime(nuevo_fecha_nacimiento, "%Y-%m-%d")
                self.collection.update_one({'numero': numero_telefono}, {'$set': {'fecha_nacimiento': nuevo_fecha_nacimiento_dt}})
                print("Fecha de nacimiento modificada exitosamente.")
            elif opcion == "4":
                nuevo_numero = input("Nuevo número de teléfono: ")
                self.collection.update_one({'numero': numero_telefono}, {'$set': {'numero': nuevo_numero}})
                print("Número de teléfono modificado exitosamente.")
            elif opcion == "5":
                nuevo_email = input("Nuevo correo electrónico: ")
                self.collection.update_one({'numero': numero_telefono}, {'$set': {'email': nuevo_email}})
                print("Correo electrónico modificado exitosamente.")
            else:
                print("Opción no válida.")
        else:
            print(f"No se encontró ningún contacto con el número de teléfono: {numero_telefono}")

    def eliminar_contacto(self):
        
        self.visualizar_agenda()

       
        numero_telefono = input("Ingrese el número de teléfono del contacto a eliminar: ")

        
        contacto = self.collection.find_one({'numero': numero_telefono})

        if contacto:
            print(f"\nEliminando contacto con el número de teléfono: {numero_telefono}")
            confirmacion = input("¿Está seguro de que desea eliminar este contacto? (S/N): ")
            if confirmacion.upper() == "S":
                self.collection.delete_one({'numero': numero_telefono})
                print("Contacto eliminado exitosamente.")
            else:
                print("Operación de eliminación cancelada.")
        else:
            print(f"No se encontró ningún contacto con el número de teléfono: {numero_telefono}")

    def solicitar_pagina_web(self):
        tiene_pagina_web = input("¿Tiene página web? (S/N): ")
        if tiene_pagina_web.upper() == "S":
            pagina_web = input("Ingrese la página web: ")
        else:
            pagina_web = "Sin página web"
        return pagina_web

    def ejecutar(self):
        while True:
            print("\n1. Agregar contacto")
            print("2. Visualizar agenda")
            print("3. Modificar contacto")
            print("4. Eliminar contacto")
            print("5. Buscar contacto")
            print("6. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                nombre = input("Nombre: ")
                while not nombre.isalpha():
                    print("Por favor, ingrese solo letras para el nombre.")
                    nombre = input("Nombre: ")

                apellido = input("Apellido: ")
                while not apellido.isalpha():
                    print("Por favor, ingrese solo letras para el apellido.")
                    apellido = input("Apellido: ")

                
                dia_nacimiento = input("Día de Nacimiento: ")
                mes_nacimiento = input("Mes de Nacimiento: ")
                anio_nacimiento = input("Año de Nacimiento: ")

                
                while not (dia_nacimiento.isdigit() and mes_nacimiento.isdigit() and anio_nacimiento.isdigit() 
                           and 1 <= int(dia_nacimiento) <= 31 and 1 <= int(mes_nacimiento) <= 12):
                    print("Por favor, ingrese una fecha de nacimiento válida.")
                    dia_nacimiento = input("Día de Nacimiento: ")
                    mes_nacimiento = input("Mes de Nacimiento: ")
                    anio_nacimiento = input("Año de Nacimiento: ")

                fecha_nacimiento = f"{anio_nacimiento}-{mes_nacimiento}-{dia_nacimiento}"

                calle = input("Calle: ")
                while not calle.replace(" ", "").isalpha():
                    print("Por favor, ingrese solo letras para el nombre de la calle.")
                    calle = input("Calle: ")

                ciudad = input("Ciudad: ")
                while not ciudad.replace(" ", "").isalpha():
                    print("Por favor, ingrese solo letras para el nombre de la ciudad.")
                    ciudad = input("Ciudad: ")

                codigo_postal = input("Código Postal: ")

                while not codigo_postal.isdigit():
                    print("Por favor, ingrese solo números para el código postal.")
                    codigo_postal = input("Código Postal: ")

                numero_exterior = input("Número Exterior: ")
                
                while not numero_exterior.isdigit():
                    print("Por favor, ingrese solo números para el número exterior.")
                    numero_exterior = input("Número Exterior: ")

                numero_interior = input("Número Interior: ")
                
                while not numero_interior.isdigit():
                    print("Por favor, ingrese solo números para el número interior.")
                    numero_interior = input("Número Interior: ")

                colonia = input("Colonia: ")
                while not colonia.replace(" ", "").isalpha():
                    print("Por favor, ingrese solo letras para el nombre de la colonia.")
                    colonia = input("Colonia: ")

                numero_telefono = input("Número de Teléfono: ")
                
                while not numero_telefono.isdigit() or len(numero_telefono) != 10:
                    print("Por favor, ingrese un número de teléfono válido (10 dígitos).")
                    numero_telefono = input("Número de Teléfono: ")

                email = input("Correo Electrónico: ")
                
                while "@" not in email or "." not in email:
                    print("Por favor, ingrese un correo electrónico válido.")
                    email = input("Correo Electrónico: ")

              
                pagina_web = self.solicitar_pagina_web()

                nuevo_contacto = Contacto(
                    nombre,
                    apellido,
                    fecha_nacimiento,
                    calle,
                    ciudad,
                    codigo_postal,
                    numero_exterior,
                    numero_interior,
                    colonia,
                    numero_telefono,
                    email,
                    pagina_web
                )
                self.agregar_contacto(nuevo_contacto)

            elif opcion == "2":
                self.visualizar_agenda()

            elif opcion == "3":
                self.modificar_contacto()

            elif opcion == "4":
                self.eliminar_contacto()
            
            elif opcion == "5":
                self.buscar_contacto()

            elif opcion == "6":
                print("Saliendo del programa. ¡Hasta luego!")
                self.cliente.close()
                break

            else:
                print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    agenda = Agenda()
    agenda.ejecutar()


