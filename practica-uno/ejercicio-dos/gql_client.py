import requests

url = 'http://localhost:8000/graphql'

query_lista_plantas = """
{
    plantas {
        id
        nombreComun
        especie
        edad
        altura
        frutos
    }
}
"""
response = requests.post(url, json={'query': query_lista_plantas})
print("Listado de plantas:")
print(response.json())

query_buscar_por_especie = """
{
    plantasPorEspecie(especie: "Cactaceae") {
        id
        nombreComun
        especie
        edad
        altura
        frutos
    }
}
"""
response = requests.post(url, json={'query': query_buscar_por_especie})
print("Plantas de la especie 'Cactaceae':")
print(response.json())

query_buscar_con_frutos = """
{
    plantasConFrutos {
        id
        nombreComun
        especie
        edad
        altura
        frutos
    }
}
"""
response = requests.post(url, json={'query': query_buscar_con_frutos})
print("Plantas que tienen frutos:")
print(response.json())

# Crear una nueva planta
mutation_crear_planta = """
mutation {
    crearPlanta(nombreComun: "Orquídea", especie: "Orchidaceae", edad: 6, altura: 25, frutos: false) {
        planta {
            id
            nombreComun
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response = requests.post(url, json={'query': mutation_crear_planta})
print("Nueva planta creada:")
print(response.json())

mutation_actualizar_planta = """
mutation {
    actualizarPlanta( id: 3, nombreComun: "Cactus Especial", especie: "Cactaceae", edad: 15, altura: 30, frutos: true) {
        planta {
            id
            nombreComun
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response = requests.post(url, json={'query': mutation_actualizar_planta})
print("Planta actualizada:")
print(response.json())

mutation_eliminar_planta = """
mutation {
    eliminarPlanta(id: 3) {
        planta {
            id
            nombreComun
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response = requests.post(url, json={'query': mutation_eliminar_planta})
print("Planta eliminada:")
print(response.json())