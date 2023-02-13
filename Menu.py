"""
1. Dar de alta un cliente con sus datos personales
2. Dar de baja un cliente
3. Mostrar los datos personales de un cliente o de todos
4. Matricular a un cliente en un deporte
5. Desmatricular a un cliente en un deporte
6. Mostrar los deportes de un cliente
7. Salir
"""
import psycopg2
import psycopg2.extras
import pprint
import sys

from Client import Client

conex = None
print("Connecting to database...")

try:
    conex = psycopg2.connect(
        dbname='polideportivo',
        host='localhost',
        user='postgres',
        password='admin123',
        port='5432')

    cursor = conex.cursor()

    cursor.execute("DROP TABLE IF EXISTS CLIENTES")
    cursor.execute("DROP TABLE IF EXISTS DEPORTES")
    cursor.execute("DROP TABLE IF EXISTS CLIENTES_DEPORTES")

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS CLIENTES ("
        "DNI VARCHAR PRIMARY KEY, NOMBRE VARCHAR, FECHA_NACIMIENTO DATE, TELEFONO VARCHAR)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS DEPORTES (DEPORTE VARCHAR PRIMARY KEY, PRECIO_HORA VARCHAR)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS CLIENTES_DEPORTES ("
        "DNI_CLIENTE VARCHAR, DEPORTE VARCHAR, HORARIOS VARCHAR, PRIMARY KEY (DNI_CLIENTE, DEPORTE))")

    cursor.execute(
        "INSERT INTO CLIENTES (DNI, NOMBRE, FECHA_NACIMIENTO, TELEFONO) "
        "VALUES ('12345678A', 'Juan Perez', '1990-01-01', '666666666')")
    cursor.execute(
        "INSERT INTO CLIENTES (DNI, NOMBRE, FECHA_NACIMIENTO, TELEFONO) "
        "VALUES ('87654321B', 'Maria Lopez', '1990-01-01', '666666666')")

    cursor.execute("INSERT INTO DEPORTES (DEPORTE, PRECIO_HORA) VALUES ('Tenis', '35€')")
    cursor.execute("INSERT INTO DEPORTES (DEPORTE, PRECIO_HORA) VALUES ('Natacion', '45€')")
    cursor.execute("INSERT INTO DEPORTES (DEPORTE, PRECIO_HORA) VALUES ('Atletismo', '20€')")
    cursor.execute("INSERT INTO DEPORTES (DEPORTE, PRECIO_HORA) VALUES ('Baloncesto', '25€')")
    cursor.execute("INSERT INTO DEPORTES (DEPORTE, PRECIO_HORA) VALUES ('Futbol', '30€')")

    cursor.execute(
        "INSERT INTO CLIENTES_DEPORTES (DNI_CLIENTE, DEPORTE, HORARIOS) "
        "VALUES ('12345678A', 'Tenis', '10:00-11:00')")

    cursor.execute(
        "INSERT INTO CLIENTES_DEPORTES (DNI_CLIENTE, DEPORTE, HORARIOS) "
        "VALUES ('12345678A', 'Natacion', '12:00-13:00')")

    conex.commit()
    cursor.close()

    print("Connection successful!")

except (Exception, psycopg2.DatabaseError) as e:
    print(f'Error {e}')
    sys.exit(1)


def high():
    dni = input("Introduce el DNI: ")
    name = input("Introduce el nombre: ")
    date = input("Introduce la fecha de nacimiento con el siguiente formato YYYY-MM-DD: ")
    phone = input("Introduce el telefono: ")
    query = "INSERT INTO CLIENTES (DNI,NOMBRE, FECHA_NACIMIENTO, TELEFONO) VALUES (%s, %s, %s, %s)"
    cursorHigh = conex.cursor()
    cursorHigh.execute(query, (name, dni, date, phone))
    conex.commit()
    cursorHigh.close()
    print("Cliente dado de alta correctamente!")
    pass


def low():
    dni = input("Introduce el DNI del cliente que quieres dar de baja: ")
    query = "DELETE FROM CLIENTES WHERE DNI = %s"
    cursorLow = conex.cursor()
    if cursorLow.execute(query, (dni,)) == 0:
        print("El cliente no existe")
        return
    conex.commit()
    cursorLow.close()
    print("Cliente dado de baja correctamente!")
    pass


def showClient():
    dni = input("Introduce el DNI del cliente que quieres consultar: ")
    query = "SELECT * FROM CLIENTES WHERE DNI = %s"
    cursorShowData = conex.cursor()
    cursorShowData.execute(query, (dni,))
    client = cursorShowData.fetchone()
    if client is None:
        print("El cliente no existe")
    else:
        obj = Client(client[0], client[1], client[2], client[3], [])
        print(obj.__data__())
        pass


def showAll():
    query = "SELECT * FROM CLIENTES"
    cursorShowData = conex.cursor()
    cursorShowData.execute(query)
    for client in cursorShowData:
        obj = Client(client[0], client[1], client[2], client[3], [])
        print(obj.__data__())
    pass


def showData():
    option = int(input("¿Quieres mostrar los datos de un cliente o de todos? (1/2): "))
    cursorShowData = conex.cursor()
    if option == 1:
        showClient()
    elif option == 2:
        showAll()
    else:
        print("Opcion incorrecta")
        return
    cursorShowData.close()
    pass


def highSport():
    dni = input("Introduce el DNI del cliente: ")
    print("Deportes : \n")
    query = "SELECT * FROM DEPORTES"
    cursorHighSport = conex.cursor()
    cursorHighSport.execute(query)
    for sports in cursorHighSport:
        print(sports)
    name = input("Introduce el nombre del deporte: ")
    time = input("Introduce el horario: ")
    query = "INSERT INTO CLIENTES_DEPORTES (DNI, NOMBRE, HORARIO) VALUES (%s, %s, %s)"
    cursorHighSport.execute(query, (dni, name, time))
    conex.commit()
    cursorHighSport.close()
    print("Cliente dado de alta correctamente!")
    pass


def lowSport():
    dni = input("Introduce el DNI del cliente: ")
    print("Deportes del cliente : \n")
    query = "SELECT DEPORTES.nombre, DEPORTES.precio, CLIENTES_DEPORTES.horario" \
            "FROM DEPORTES, CLIENTES_DEPORTES" \
            "WHERE DEPORTES.nombre = CLIENTES_DEPORTES.nombre AND CLIENTES_DEPORTES.dni = %s"
    cursorLowSport = conex.cursor()
    cursorLowSport.execute(query, (dni,))
    for sports in cursorLowSport:
        print(sports)

    query = "DELETE FROM CLIENTES_DEPORTES WHERE DNI = %s"
    if cursorLowSport.execute(query, (dni,)) == 0:
        print("El cliente no existe")
        return
    conex.commit()
    cursorLowSport.close()
    print("Cliente dado de baja correctamente!")
    pass


def sport():
    dni = input("Introduce el DNI del cliente que quieres consultar: ")
    query = "SELECT DEPORTES.nombre, CLIENTES_DEPORTES.horario" \
            "FROM DEPORTES, CLIENTES_DEPORTES" \
            "WHERE DEPORTES.nombre = CLIENTES_DEPORTES.nombre AND CLIENTES_DEPORTES.dni = %s"

    cursorSports = conex.cursor()
    cursorSports.execute(query, (dni,))
    obj = Client("", "", "", "", [])
    for sports in cursorSports:
        obj = (sports[0], sports[1], sports[2])
        obj.sports.append(obj)

    print(obj.__sports__())

    cursorSports.close()
    pass


def menu():
    while True:
        print("""
        1. Dar de alta un cliente con sus datos personales
        2. Dar de baja un cliente
        3. Mostrar los datos personales de un cliente o de todos
        4. Matricular a un cliente en un deporte
        5. Desmatricular a un cliente en un deporte
        6. Mostrar los deportes de un cliente
        7. Salir
        """)
        option = int(input("Selecciona la opción que vas a realizar: "))

        match option:
            case 1:
                high()
            case 2:
                low()
            case 3:
                showData()
            case 4:
                highSport()
            case 5:
                lowSport()
            case 6:
                sport()
            case 7:
                break
            case _:
                print("Opcion no valida")

        print("¿Quieres realizar otra operacion? (S/N)")
        answer = input().upper()
        if answer == "S":
            continue
        else:
            print("Hasta pronto!")
            break


if conex is not None:
    while True:
        menu()
        break

