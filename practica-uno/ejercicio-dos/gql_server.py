from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Boolean, List, Schema, Field, Mutation

class Planta(ObjectType):
    id = Int()
    nombre_comun = String()
    especie = String()
    edad = Int()
    altura = Int()
    frutos = Boolean()

class Query(ObjectType):
    plantas = List(Planta)
    plantas_por_especie = List(Planta, especie=String())
    plantas_con_frutos = List(Planta)

    def resolve_plantas(root, info):
        return plantas
    
    def resolve_plantas_por_especie(root, info, especie):
        return [planta for planta in plantas if planta.especie == especie]
    
    def resolve_plantas_con_frutos(root, info):
        return [planta for planta in plantas if planta.frutos]

class CrearPlanta(Mutation):
    class Arguments:
        nombre_comun = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()

    planta = Field(Planta)

    def mutate(root, info, nombre_comun, especie, edad, altura, frutos):
        nueva_planta = Planta(
            id=len(plantas) + 1,
            nombre_comun=nombre_comun,
            especie=especie,
            edad=edad,
            altura=altura,
            frutos=frutos
        )
        plantas.append(nueva_planta)

        return CrearPlanta(planta=nueva_planta)

class ActualizarPlanta(Mutation):
    class Arguments:
        id = Int()
        nombre_comun = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()

    planta = Field(Planta)

    def mutate(root, info, id, nombre_comun, especie, edad, altura, frutos):
        for planta in plantas:
            if planta.id == id:
                planta.nombre_comun = nombre_comun
                planta.especie = especie
                planta.edad = edad
                planta.altura = altura
                planta.frutos = frutos
                return ActualizarPlanta(planta=planta)
        return None

class EliminarPlanta(Mutation):
    class Arguments:
        id = Int()

    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return EliminarPlanta(planta=planta)
        return None

class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    actualizar_planta = ActualizarPlanta.Field()
    eliminar_planta = EliminarPlanta.Field()

plantas = [
    Planta(
        id=1, nombre_comun="Cactus", especie="Cactaceae", edad=12, altura=20, frutos=False
    ),
    Planta(id=2, nombre_comun="Rosa", especie="Rosa", edad=24, altura=30, frutos=True),
]

schema = Schema(query=Query, mutation=Mutations)

class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()