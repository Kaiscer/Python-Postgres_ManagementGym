"""
• Crea una clase llamada Clientes con los siguientes atributos para guardar los datos personales de los clientes:
nombre completo, dni, fecha de nacimiento y teléfono.
• Los deportes que ofrece el polideportivo son: tenis, natación, atletismo, baloncesto y futbol.
• Los datos que deben guardarse de los deportes son nombre del deporte y precio/hora.
• La clase Clientes tendrá un método llamado __datos__ que permita mostrar los datos
personales de un cliente.
• La clase Clientes tendrá un método llamado __deportes__ que permita mostrar el nombre de
los deportes con su precio en los que está matriculado un cliente.
• Al matricular a un cliente en un deporte se guardará el nombre del deporte y el horario
elegido.
"""
from dataclasses import dataclass


@dataclass
class Client:
    def __init__(self, dni, name, birth_date, phone, sports):
        self.dni = dni
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.sports = sports

    def __data__(self):
        return f"""
        Dni: {self.dni}
        Name: {self.name}
        Birth date: {self.birth_date}
        Phone: {self.phone}
        """


class Registration:
    def __init__(self, client, sport, price):
        self.client = client
        self.sport = sport
        self.price = price

    def __dataSports__(self, sport):
        return f"""
        Client: {self.client}
        Sport: {self.sport}
        """

