class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.historial = []

    def insertarHistorial(self, transaccion):
        self.historial.append(transaccion)
    def getHistorial(self):
        return self.historial
    
    def getNumero(self):
        return self.numero

    def getNombre(self):
        return self.nombre

    def getSaldo(self):
        return self.saldo

    def getContactos(self):
        return self.contactos

    def setNumero(self, numero):
        self.numero = numero

    def setNombre(self, nombre):
        self.nombre = nombre

    def setSaldo(self, saldo):
        self.saldo = saldo

    def setContactos(self, contactos):
        self.contactos = contactos

    def agregarContacto(self, contacto):
        self.contactos.append(contacto)

    def __str__(self):
        return "Numero: " + self.numero + " Nombre: " + self.nombre + " Saldo: " + str(self.saldo) + " Contactos: " + str(self.contactos)

