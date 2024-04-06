import requests

url = "http://localhost:8000/"

ruta_get = url + "pacientes"
get_response = requests.get(ruta_get)
print("GET todos los pacientes:")
print(get_response.text)

ci = "790356"
ruta_get = url + f"pacientes/{ci}"
get_response = requests.get(ruta_get)
print("\nGET paciente por CI:")
print(get_response.text)

diagnostico = "Diabetes"
ruta_get = url + f"pacientes?diagnostico={diagnostico}"
get_response = requests.get(ruta_get)
print("\nGET pacientes por diagnóstico:")
print(get_response.text)

doctor = "Pedro Pérez"
ruta_get = url + f"pacientes?doctor={doctor}"
get_response = requests.get(ruta_get)
print("\nGET pacientes por doctor:")
print(get_response.text)

ruta_post = url + "pacientes"
nuevo_paciente = {
    "ci": "789012",
    "nombre": "Ana",
    "apellido": "García",
    "edad": 40,
    "genero": "Femenino",
    "diagnostico": "Hipertension",
    "doctor": "Maria Lopez"
}
post_response = requests.post(ruta_post, json=nuevo_paciente)
print("\nPOST nuevo paciente:")
print(post_response.text)

ci = "789012"
datos_actualizados = {
    "diagnostico": "Diabetes"
}
ruta_put = url + f"pacientes/{ci}"
put_response = requests.put(ruta_put, json=datos_actualizados)
print("\nPUT actualizar paciente:")
print(put_response.text)

ci = "789012"
ruta_delete = url + f"pacientes/{ci}"
delete_response = requests.delete(ruta_delete)
print("\nDELETE eliminar paciente:")
print(delete_response.text)