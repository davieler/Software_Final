from datetime import date
import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
class TestBilleteraEndpoints(unittest.TestCase):

    # Test case for pagar endpoint
    def test_pagar(self):
        # Success case
        response = client.get("/billetera/pagar/minumero=123&numerodestino=456&valor=100")
        assert response.status_code == 200
        today_date = date.today()
        assert response.json() == {"message": f"Pago realizado con éxito en {today_date}"}

        # Error cases
        # Case 1: Non-existent payer number
        response = client.get("/billetera/pagar/minumero=999&numerodestino=456&valor=100")
        assert response.status_code == 404
        assert response.json() == {"detail": "El numero de telefono no existe"}

        # Case 2: Non-existent payee number
        response = client.get("/billetera/pagar/minumero=123&numerodestino=999&valor=100")
        assert response.status_code == 404
        assert response.json() == {"detail": "El numero de telefono no existe"}

        # Case 3: Insufficient balance
        response = client.get("/billetera/pagar/minumero=123&numerodestino=456&valor=500")
        assert response.status_code == 200
        assert response.json() == {"message": "Saldo insuficiente"}


    # Test case for historial endpoint
    def test_historial(self):
        # Success case
        response = client.get("/billetera/historial/minumero=123")
        assert response.status_code == 200
        assert "saldo" in response.json()
        assert "historial" in response.json()

        # Error case: Non-existent number
        response = client.get("/billetera/historial/minumero=999")
        assert response.status_code == 404
        assert response.json() == {"detail": "El numero de telefono no existe"}

if __name__ == "__main__":
    unittest.main()