"""
Se debe soportar las operaciones:
- Contactos: Lista los contactos de un número de teléfono con sus nombres.
- Pagar: Transfiere un valor a otro número (debe ser un contacto). La cuenta debe tener
saldo suficiente para hacer la transferencia.
- Historial: Muestra el saldo y la lista de operaciones, tanto de envío como de recepción
de dinero.
"""
from fastapi import HTTPException
from fastapi import FastAPI
from Cuenta import Cuenta
from datetime import date


app = FastAPI()

BD = []
BD.append(Cuenta("21345", "Arnaldo", 200, ["123", "456"]))
BD.append(Cuenta("123", "Luisa", 400, ["456"]))
BD.append(Cuenta("456", "Andrea", 300, ["21345"]))
BD.append(Cuenta("4344", "vacio", 0, []))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/billetera/contactos/minumero={mynumber}", status_code=200)
def read_contactos(mynumber: str):
    if not mynumber.isnumeric():
        raise HTTPException(status_code=422, detail="type error")
    formatted_contactos = []
    for i in BD:
        if i.getNumero() == mynumber:
            contactos = i.getContactos()
            for j in contactos:
                for k in BD:
                    if j == k.getNumero():
                        formatted_contactos.append({k.getNumero(), k.getNombre()})
    if formatted_contactos:
        return {"contactos": formatted_contactos}
    else:
        raise HTTPException(status_code=404, detail="El numero de telefono no existe")

@app.get("/billetera/pagar/minumero={mynumber}&numerodestino={numerodestino}&valor={valor}")
def pagar(mynumber: str, numerodestino: str, valor: int):
    #Verificar que ambos numeros de cuenta existen 
    # y guardar los index de donde están esas cuentas en la lista para no iterar nuevamente
    accounts = [None, None]
    for cuenta in BD:
        if cuenta.getNumero() == mynumber:
            accounts[0] = cuenta #cuenta que paga
        if cuenta.getNumero() == numerodestino:
            accounts[1] = cuenta #cuenta que recibe
    
    #verificar si hay saldo suficiente para pagar
    if (accounts[0] != None) and (accounts[1] != None):
        if accounts[0].getSaldo() < valor:
            return {"message": "Saldo insuficiente"}
        else:
            accounts[1].setSaldo(accounts[1].getSaldo() + valor)
            accounts[0].setSaldo(accounts[0].getSaldo() - valor)
            #insertar en el historial de ambas cuentas
            accounts[0].insertarHistorial(f"Pago realizado de {valor} a {accounts[1].getNombre()}")
            accounts[1].insertarHistorial(f"Pago recibido de {valor} de {accounts[0].getNombre()}")
            
            today_date = date.today()
            return {"message": f"Pago realizado con éxito en {today_date}"}
    else: 
        raise HTTPException(status_code=404, detail="El numero de telefono no existe")

@app.get("/billetera/historial/minumero={mynumber}")
def historial(mynumber: str):
    for i in BD:
        if i.getNumero() == mynumber:
            return {"saldo": i.getSaldo(), "historial": i.getHistorial()}
        
    raise HTTPException(status_code=404, detail="El numero de telefono no existe")
