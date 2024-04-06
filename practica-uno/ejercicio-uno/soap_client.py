from zeep import Client

client = Client('http://localhost:8000')

result = client.service.Suma(4, 5)
print("Resultado de la suma:", result)

result = client.service.Resta(10, 3)
print("Resultado de la resta:", result)

result = client.service.Multiplicacion(7, 8)
print("Resultado de la multiplicación:", result)

result = client.service.Divicion(20, 4)
print("Resultado de la división:", result)