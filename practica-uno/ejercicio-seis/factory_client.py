import requests

url = "http://localhost:8000/"

# El ID es None porque si no se proporcionaba ese dato, el ID se añadiría al final
# de todos los datos cuando se agregara al diccionario, por lo que al menos quedaría
# en orden de esta forma.
print("\nPOST nuevo animal:")
nuevo_animal = {
    "id": None,
    "nombre": "Tigre",
    "tipo": "Mamifero",
    "especie": "Felino",
    "genero": "Masculino",
    "edad": 9,
    "peso": "29kg",
}
ruta_post = url + "animales"
post_response = requests.post(ruta_post, json=nuevo_animal)
print(post_response.text)

nuevo_animal = {
    "id": None,
    "nombre": "Cobra Egipcia",
    "tipo": "Reptil",
    "especie": "Naja haje",
    "genero": "Femenino",
    "edad": 7,
    "peso": "10kg",
}
ruta_post = url + "animales"
post_response = requests.post(ruta_post, json=nuevo_animal)
print("\n----------------------------------")
print(post_response.text)

nuevo_animal = {
    "id": None,
    "nombre": "Leon",
    "tipo" : "Mamifero",
    "especie": "Felino",
    "genero": "Masculino",
    "edad": 5,
    "peso": "27kg"
}
ruta_post = url + "animales"
post_response = requests.post(ruta_post, json=nuevo_animal)
print("\n------------------------------------")
print(post_response.text)

ruta_get = url + "animales"
get_response = requests.get(ruta_get)
print("\nGET todos los animales:")
print(get_response.text)

especie = "Felino"
ruta_get = url + f"animales?especie={especie}"
get_response = requests.get(ruta_get)
print("\nGET animales por especie:")
print(get_response.text)

genero = "Masculino"
ruta_get = url + f"animales?genero={genero}"
get_response = requests.get(ruta_get)
print("\nGET animales por género:")
print(get_response.text)

animal_id = 3
datos_actualizados = {
    "nombre": "Leon Rey",
    "edad": 6
}
ruta_put = url + f"animales/{animal_id}"
put_response = requests.put(ruta_put, json=datos_actualizados)
print("\nPUT actualizar animal:")
print(put_response.text)

animal_id = 2
ruta_delete = url + f"animales/{animal_id}"
delete_response = requests.delete(ruta_delete)
print("\nDELETE eliminar animal:")
print(delete_response.text)