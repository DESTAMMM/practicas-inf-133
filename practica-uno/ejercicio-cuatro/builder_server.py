from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class Paciente:
    def __init__(self, ci, nombre, apellido, edad, genero, diagnostico, doctor):
        self.ci = ci
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.genero = genero
        self.diagnostico = diagnostico
        self.doctor = doctor

class PacienteBuilder:
    def __init__(self):
        self.ci = None
        self.nombre = None
        self.apellido = None
        self.edad = None
        self.genero = None
        self.diagnostico = None
        self.doctor = None

    def set_ci(self, ci):
        self.ci = ci
        return self

    def set_nombre(self, nombre):
        self.nombre = nombre
        return self

    def set_apellido(self, apellido):
        self.apellido = apellido
        return self

    def set_edad(self, edad):
        self.edad = edad
        return self

    def set_genero(self, genero):
        self.genero = genero
        return self

    def set_diagnostico(self, diagnostico):
        self.diagnostico = diagnostico
        return self

    def set_doctor(self, doctor):
        self.doctor = doctor
        return self

    def build(self):
        return Paciente(self.ci, self.nombre, self.apellido, self.edad, self.genero, self.diagnostico, self.doctor)

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
        paciente_builder = PacienteBuilder()
        paciente = paciente_builder \
            .set_ci(data.get('ci')) \
            .set_nombre(data.get('nombre')) \
            .set_apellido(data.get('apellido')) \
            .set_edad(data.get('edad')) \
            .set_genero(data.get('genero')) \
            .set_diagnostico(data.get('diagnostico')) \
            .set_doctor(data.get('doctor')) \
            .build()
        pacientes.append(paciente.__dict__)
        return paciente.__dict__

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
    def read_data(handler):
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
            data = HTTPResponseHandler.read_data(self)
            paciente = PacientesService.add_paciente(data)
            HTTPResponseHandler.handle_response(self, 201, paciente)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = self.path.split("/")[-1]
            data = HTTPResponseHandler.read_data(self)
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

def run(server_class=HTTPServer, handler_class=PacienteHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()