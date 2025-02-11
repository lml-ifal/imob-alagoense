import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

PROPERTIES_FILE = "properties.txt"
CUSTOMERS_FILE = "customers.txt"

STYLE = """
<style>
    body {
        font-family: Arial, sans-serif;
        margin: 20px;
        text-align: center;
    }
    table {
        width: 80%;
        margin: 20px auto;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    th {
        background-color: #f4f4f4;
    }
    a {
        display: block;
        margin-top: 20px;
    }
    form {
        margin: 20px auto;
        padding: 10px;
        width: 20%;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #f9f9f9;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    form label {
        margin-bottom: 8px;
        font-weight: bold;
    }
    form input, form select, form button {
        width: 75%;
        padding: 6px;
        margin-bottom: 8px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    form button {
        background-color: #4CAF50;
        color: white;
        font-size: 14px;
        cursor: pointer;
    }
    form button:hover {
        background-color: #45a049;
    }
</style>
"""


def load_properties():
    properties = []
    if os.path.exists(PROPERTIES_FILE):
        with open(PROPERTIES_FILE, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 4:
                    properties.append({
                        "id": int(parts[0]),
                        "address": parts[1],
                        "budget": float(parts[2]),
                        "status": parts[3]
                    })
    return properties


def save_property(property):
    with open(PROPERTIES_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"{property['id']}|{property['address']}|{property['budget']}|{property['status']}\n")


def load_customers():
    customers = []
    if os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    customers.append({
                        "id": int(parts[0]),
                        "name": parts[1],
                        "contact": parts[2]
                    })
    return customers


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.render_html().encode("utf-8"))
        elif self.path == '/clientes':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.render_customers_html().encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        params = parse_qs(post_data)

        address = params.get("address", [""])[0]
        budget = params.get("budget", [""])[0]
        status = params.get("status", [""])[0]

        properties = load_properties()
        new_property = {
            "id": len(properties) + 1,
            "address": address,
            "budget": float(budget),
            "status": status
        }
        save_property(new_property)

        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def render_html(self):
        properties = load_properties()

        html = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lista de Imóveis</title>
            {STYLE}
        </head>
        <body>
            <h1>Imóveis Disponíveis</h1>
            <form method="post">
                <label>Endereço:</label>
                <input type="text" name="address" required>
                <label>Valor:</label>
                <input type="number" name="budget" step="0.01" required>
                <label>Status:</label>
                <select name="status">
                    <option value="disponível">Disponível</option>
                    <option value="alugado">Alugado</option>
                    <option value="vendido">Vendido</option>
                </select>
                <button type="submit">Cadastrar Imóvel</button>
            </form>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Endereço</th>
                    <th>Valor</th>
                    <th>Status</th>
                </tr>
        """
        for property in properties:
            html += f"""
                <tr>
                    <td>{property['id']}</td>
                    <td>{property['address']}</td>
                    <td>R$ {property['budget']:.2f}</td>
                    <td>{property['status']}</td>
                </tr>
            """
        html += """</table>
        <a href='/clientes'>Ver Clientes</a>
        </body></html>"""
        return html


if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Servidor rodando em http://localhost:8000")
    print("Acesse http://localhost:8000/clientes para ver os clientes")
    httpd.serve_forever()
