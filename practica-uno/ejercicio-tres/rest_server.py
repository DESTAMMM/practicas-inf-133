from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

pacientes = [
    {
        "ci": "786147",
        "nombre": "Jose",
        "apellido": "Morales",
        "edad": 35,
        "genero": "Masculino",
        "diagnostico": "Diabetes",
        "doctor": "Juan Bustamante",
    },
    {
        "ci": "790356",
        "nombre": "Miguel",
        "apellido": "Suares",
        "edad": 28,
        "genero": "Masculino",
        "diagnostico": "Artritis",
        "doctor": "Pedro Pérez",
    }
]

class PacientesService:
    @staticmethod
    def find_paciente(ci):
        return next(
            (paciente for paciente in pacientes if paciente["ci"] == ci),
            None,
        )

    @staticmethod
    def filter_pacientes_by_diagnostico(diagnostico):
        return [
            paciente for paciente in pacientes if paciente["diagnostico"] == diagnostico
        ]

    @staticmethod
    def filter_pacientes_by_doctor(doctor):
        return [
            paciente for paciente in pacientes if paciente["doctor"] == doctor
        ]

    @staticmethod
    def add_paciente(data):
        pacientes.append(data)
        return data

    @staticmethod
    def update_paciente(ci, data):
        paciente = PacientesService.find_paciente(ci)
        if paciente:
            paciente.update(data)
            return paciente
        else:
            return None

    @staticmethod
    def delete_paciente(ci):
        for i, paciente in enumerate(pacientes):
            if paciente["ci"] == ci:
                return pacientes.pop(i)
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

        if parsed_path.path == "/pacientes":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = PacientesService.filter_pacientes_by_diagnostico(diagnostico)
                if pacientes_filtrados:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filtrados = PacientesService.filter_pacientes_by_doctor(doctor)
                if pacientes_filtrados:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
        elif self.path.startswith("/pacientes/"):
            ci = self.path.split("/")[-1]
            paciente = PacientesService.find_paciente(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/pacientes":
            data = HTTPResponseHandler.handle_reader(self)
            paciente = PacientesService.add_paciente(data)
            HTTPResponseHandler.handle_response(self, 201, paciente)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = self.path.split("/")[-1]
            data = HTTPResponseHandler.handle_reader(self)
            paciente = PacientesService.update_paciente(ci, data)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, paciente)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Paciente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = self.path.split("/")[-1]
            paciente = PacientesService.delete_paciente(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, paciente)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Paciente no encontrado"}
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