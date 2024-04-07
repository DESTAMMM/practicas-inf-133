from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class Animal:
    def __init__(self, id, nombre, tipo, especie, genero, edad, peso):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso

class Mamifero(Animal):
    def __init__(self, id, nombre, especie, genero, edad, peso):
        super().__init__(id, nombre, "Mamifero",  especie, genero, edad, peso)

class Ave(Animal):
    def __init__(self, id, nombre, especie, genero, edad, peso):
        super().__init__(id, nombre, "Ave", especie, genero, edad, peso)

class Reptil(Animal):
    def __init__(self, id, nombre, especie, genero, edad, peso):
        super().__init__(id, nombre, "Reptil", especie, genero, edad, peso)

class Anfibio(Animal):
    def __init__(self, id, nombre, especie, genero, edad, peso):
        super().__init__(id, nombre, "Anfibio", especie, genero, edad, peso)

class Pez(Animal):
    def __init__(self, id, nombre, especie, genero, edad, peso):
        super().__init__(id, nombre, "Pez", especie, genero, edad, peso)

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type, id, nombre, especie, genero, edad, peso):
        if animal_type == "Mamifero":
            return Mamifero(id, nombre, especie, genero, edad, peso)
        elif animal_type == "Ave":
            return Ave(id, nombre, especie, genero, edad, peso)
        elif animal_type == "Reptil":
            return Reptil(id, nombre, especie, genero, edad, peso)
        elif animal_type == "Anfibio":
            return Anfibio(id, nombre, especie, genero, edad, peso)
        elif animal_type == "Pez":
            return Pez(id, nombre, especie, genero, edad, peso)
        else:
            raise ValueError("Tipo de animal no válido")

class AnimalService:
    animals = {}

    @staticmethod
    def add_animal(data):
        animal_keys = AnimalService.animals.keys()
        new_id = max(animal_keys) + 1 if animal_keys else 1
        animal_type = data.get("tipo", None)
        nombre = data.get("nombre", None)
        especie = data.get("especie", None)
        genero = data.get("genero", None)
        edad = data.get("edad", None)
        peso = data.get("peso", None)

        animal = AnimalFactory.create_animal(animal_type, new_id, nombre, especie, genero, edad, peso)
        AnimalService.animals[new_id] = animal.__dict__
        return animal.__dict__

    @staticmethod
    def list_animals():
        return list(AnimalService.animals.values())

    @staticmethod
    def find_animals_by_especie(especie):
        return [animal for animal in AnimalService.animals.values() if animal["especie"] == especie]

    @staticmethod
    def find_animals_by_genero(genero):
        return [animal for animal in AnimalService.animals.values() if animal["genero"] == genero]

    @staticmethod
    def get_animal_by_id(animal_id):
        return AnimalService.animals.get(animal_id)

    @staticmethod
    def update_animal(animal_id, data):
        animal = AnimalService.animals.get(animal_id)
        if animal:
            for key, value in data.items():
                animal[key] = value
            return animal
        return None

    @staticmethod
    def delete_animal(animal_id):
        return AnimalService.animals.pop(animal_id, None)

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        data = handler.rfile.read(content_length)
        return json.loads(data.decode("utf-8"))

class RESTRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.animal_service = AnimalService()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animales = self.animal_service.find_animals_by_especie(especie)
                if animales:
                    HTTPResponseHandler.handle_response(self, 200, animales)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                animales = self.animal_service.find_animals_by_genero(genero)
                if animales:
                    HTTPResponseHandler.handle_response(self, 200, animales)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                animales = self.animal_service.list_animals()
                HTTPResponseHandler.handle_response(self, 200, animales)
        elif parsed_path.path.startswith("/animales/"):
            animal_id = int(parsed_path.path.split("/")[-1])
            animal = self.animal_service.get_animal_by_id(animal_id)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, animal)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Animal no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/animales":
            data = HTTPResponseHandler.handle_reader(self)
            response_data = self.animal_service.add_animal(data)
            HTTPResponseHandler.handle_response(self, 201, response_data)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPResponseHandler.handle_reader(self)
            response_data = self.animal_service.update_animal(animal_id, data)
            if response_data:
                HTTPResponseHandler.handle_response(self, 200, response_data)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Animal no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            response_data = self.animal_service.delete_animal(animal_id)
            if response_data:
                HTTPResponseHandler.handle_response(self, 200, response_data)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Animal no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()