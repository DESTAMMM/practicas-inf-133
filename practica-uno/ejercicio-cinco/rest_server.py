from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class AnimalService:
    animals = [
        {
            "id": 1,
            "nombre": "Tigre",
            "especie": "Felino",
            "genero": "Masculino",
            "edad": 9,
            "peso": "29kg",
        },
        {
            "id": 2,
            "nombre": "Perro",
            "especie": "Canino",
            "genero": "Femenino",
            "edad": 7,
            "peso": "16kg",
        }
    ]

    @staticmethod
    def add_animal(data):
        animal_keys = [animal["id"] for animal in AnimalService.animals]
        new_id = max(animal_keys) + 1 if animal_keys else 1
        data["id"] = new_id
        AnimalService.animals.append(data)
        return data

    @staticmethod
    def list_animals():
        return AnimalService.animals

    @staticmethod
    def find_animals_by_especies(especie):
        return [animal for animal in AnimalService.animals if animal["especie"] == especie]

    @staticmethod
    def find_animals_by_genero(genero):
        return [animal for animal in AnimalService.animals if animal["genero"] == genero]

    @staticmethod
    def update_animal(animal_id, data):
        for animal in AnimalService.animals:
            if animal["id"] == animal_id:
                animal.update(data)
                return animal
        return None

    @staticmethod
    def delete_animal(animal_id):
        for i, animal in enumerate(AnimalService.animals):
            if animal["id"] == animal_id:
                return AnimalService.animals.pop(i)
        return None

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
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animales = AnimalService.find_animals_by_especies(especie)
                if animales:
                    HTTPResponseHandler.handle_response(self, 200, animales)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                animales = AnimalService.find_animals_by_genero(genero)
                if animales:
                    HTTPResponseHandler.handle_response(self, 200, animales)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                animales = AnimalService.list_animals()
                HTTPResponseHandler.handle_response(self, 200, animales)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/animales":
            data = HTTPResponseHandler.handle_reader(self)
            animal = AnimalService.add_animal(data)
            HTTPResponseHandler.handle_response(self, 201, animal)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPResponseHandler.handle_reader(self)
            animal = AnimalService.update_animal(animal_id, data)
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

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            animal = AnimalService.delete_animal(animal_id)
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