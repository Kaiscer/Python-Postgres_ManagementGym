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
        "dni VARCHAR PRIMARY KEY, nombre VARCHAR, fecha_nacimiento DATE, telefono VARCHAR)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS DEPORTES (deporte VARCHAR PRIMARY KEY, precio_hora VARCHAR)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS CLIENTES_DEPORTES ("
        "dni_cliente VARCHAR, deporte VARCHAR, horario VARCHAR, PRIMARY KEY (dni_cliente, deporte))")

    cursor.execute(
        "INSERT INTO CLIENTES (dni, nombre, fecha_nacimiento, telefono) "
        "VALUES ('12345678A', 'Juan Perez', '1990-01-01', '666666666')")
    cursor.execute(
        "INSERT INTO CLIENTES (dni, nombre, fecha_nacimiento, telefono) "
        "VALUES ('87654321B', 'Maria Lopez', '1990-01-01', '666666666')")

    cursor.execute("INSERT INTO DEPORTES (deporte, precio_hora) VALUES ('Tenis', '35€')")
    cursor.execute("INSERT INTO DEPORTES (deporte, precio_hora) VALUES ('Natacion', '45€')")
    cursor.execute("INSERT INTO DEPORTES (deporte, precio_hora) VALUES ('Atletismo', '20€')")
    cursor.execute("INSERT INTO DEPORTES (deporte, precio_hora) VALUES ('Baloncesto', '25€')")
    cursor.execute("INSERT INTO DEPORTES (deporte, precio_hora) VALUES ('Futbol', '30€')")

    cursor.execute(
        "INSERT INTO CLIENTES_DEPORTES (dni_cliente, deporte, horario) "
        "VALUES ('12345678A', 'Tenis', '10:00-11:00')")

    cursor.execute(
        "INSERT INTO CLIENTES_DEPORTES (dni_cliente, deporte, horario) "
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
    query = "INSERT INTO CLIENTES_DEPORTES (dni, nombre, horario) VALUES (%s, %s, %s)"
    cursorHighSport.execute(query, (dni, name, time))
    conex.commit()
    cursorHighSport.close()
    print("Cliente dado de alta correctamente!")
    pass


def lowSport():
    try:
        dni = input("Introduce el DNI del cliente: ")
        cursorLowSport = conex.cursor()
        query = "SELECT * FROM CLIENTES_DEPORTES WHERE dni_cliente = %s"
        cursorLowSport.execute(query, (dni,))
        client = cursorLowSport.fetchall()
        if client is None:
            print("El cliente no existe")
            return
        else:
            print("Deportes del cliente: \n")
            listSport = []
            for sports in client:
                print(sports)
                listSport.append(sports[1])
            sportLow = input("Introduce el deporte que quieres dar de baja: ")
            if sportLow not in listSport:
                print("El deporte no existe")
                return
            else:
                query = "DELETE FROM CLIENTES_DEPORTES WHERE dni_cliente = %s AND deporte = %s"
                cursorLowSport.execute(query, (dni, sportLow))
                conex.commit()
                cursorLowSport.close()
                print("Deporte dado de baja correctamente!")
                return
    except (Exception, psycopg2.DatabaseError) as e:
        print(f'Error {e}')

    pass


def sport():
    dni = input("Introduce el DNI del cliente que quieres consultar: ")
    cursorSports = conex.cursor()
    query = "SELECT * FROM CLIENTES WHERE dni = %s"
    cursorSports.execute(query, (dni,))
    conex.commit()
    client = cursorSports.fetchone()
    if client is None:
        print("El cliente no existe")
        return
    query = "SELECT * FROM CLIENTES_DEPORTES WHERE dni_cliente = %s"
    cursorSports.execute(query, (client[0],))
    conex.commit()
    listSport = cursorSports.fetchall()
    if listSport is None:
        print("El cliente no tiene deportes")
    else:
        print("Deportes del cliente: \n")
        for sports in listSport:
            cursorSports.execute("SELECT * FROM DEPORTES WHERE deporte = %s", (sports[1],))
            conex.commit()
            sportC = cursorSports.fetchone()
            print("Deporte: " + sportC[0] + " Horario: " + sports[2])

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

