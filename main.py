import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

PROPERTIES_FILE = "properties.txt"
CUSTOMERS_FILE = "customers.txt"

STYLE = """
    <style>
        body {
            background-color: #1a1a1a;
            color: #f5c518;
            font-family: 'Arial', sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        header {
            background: linear-gradient(90deg, #8c1c13, #1a1a1a);
            padding: 20px;
        }
        img.logo {
            width: 150px;
            display: block;
            margin: 0 auto;
        }
        h1 {
            font-size: 2.5em;
            margin: 10px 0;
        }
        .container {
            width: 80%;
            margin: 20px auto;
            padding: 20px;
            background: #222;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #f5c518;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #8c1c13;
            color: white;
        }
        .form-container {
            background: #333;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        label, input, select, button {
            display: block;
            width: 80%;
            margin: 10px auto;
            padding: 10px;
            border-radius: 5px;
        }
        button {
            background-color: #f5c518;
            color: #1a1a1a;
            font-weight: bold;
            cursor: pointer;
            border: none;
        }
        button:hover {
            background-color: #ffd700;
        }
        a {
            text-decoration: none;
        }
        .nav-buttons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        .nav-buttons a button {
            width: 200px;
            padding: 10px;
            font-size: 1.2em;
        }
    </style>
"""

def load_data(file_path, num_fields):
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == num_fields:
                    entry = {str(i): parts[i] for i in range(num_fields)}
                    data.append(entry)
    return data

def save_data(file_path, entry):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write("|".join(entry.values()) + "\n")

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.render_html("properties").encode("utf-8"))
        elif self.path == '/clientes':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.render_html("customers").encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        params = parse_qs(post_data)

        if self.path == "/clientes":
            new_entry = {"0": str(len(load_data(CUSTOMERS_FILE, 3)) + 1),
                         "1": params.get("name", [""])[0],
                         "2": params.get("contact", [""])[0]}
            save_data(CUSTOMERS_FILE, new_entry)
            self.send_response(303)
            self.send_header("Location", "/clientes")
            self.end_headers()
        else:
            new_entry = {"0": str(len(load_data(PROPERTIES_FILE, 4)) + 1),
                         "1": params.get("address", [""])[0],
                         "2": params.get("budget", [""])[0],
                         "3": params.get("status", [""])[0]}
            save_data(PROPERTIES_FILE, new_entry)
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()

    def render_html(self, page_type):
        data = load_data(PROPERTIES_FILE if page_type == "properties" else CUSTOMERS_FILE, 4 if page_type == "properties" else 3)
        headers = ["ID", "Endereço", "Valor", "Status"] if page_type == "properties" else ["ID", "Nome", "Contato"]
        
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lista de {"Imóveis" if page_type == "properties" else "Clientes"}</title>
            {STYLE}
        </head>
        <body>
            <header>
                <img src="logo.jpg" alt="Logo" class="logo">
                <h1>{"Imóveis Disponíveis" if page_type == "properties" else "Clientes Cadastrados"}</h1>
            </header>
            <div class="container">
                <form method="post" action="{'' if page_type == 'properties' else '/clientes'}">
        """
        
        form_fields = ["address", "budget", "status"] if page_type == "properties" else ["name", "contact"]
        form_labels = ["Endereço", "Valor", "Status"] if page_type == "properties" else ["Nome", "Contato"]
        
        for label, field in zip(form_labels, form_fields):
            if field == "status":
                html += f"""
                    <label>{label}:</label>
                    <select name="{field}" required>
                        <option value="Disponível">Disponível</option>
                        <option value="Vendido">Vendido</option>
                        <option value="Reservado">Reservado</option>
                    </select>
                """
            else:
                html += f'<label>{label}:</label><input type="text" name="{field}" required>'
        
        html += '<button type="submit">Cadastrar</button></form><table><tr>'
        
        for header in headers:
            html += f'<th>{header}</th>'
        html += '</tr>'
        
        for entry in data:
            html += '<tr>' + ''.join(f'<td>{entry[str(i)]}</td>' for i in range(len(headers))) + '</tr>'
        

        html += """
            </table>
            <div class="nav-buttons" style="margin-top: 20px;">
        """
        
        if page_type == "properties":
            html += '<a href="/clientes"><button style="margin-right: 10px;">Ir para Clientes</button></a>'
        else:
            html += '<a href="/"><button style="margin-right: 10px;">Voltar para Imóveis</button></a>'
        
        html += """
            </div>
            </div>
        </body></html>
        """
        
        return html

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Servidor rodando em http://localhost:8000")
    httpd.serve_forever()
