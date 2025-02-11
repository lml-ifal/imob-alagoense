def save_customer(customer):
    """Salva um cliente no arquivo customers.txt"""
    with open(CUSTOMERS_FILE, "a", encoding="utf-8") as file:
        file.write(f"{customer['id']}|{customer['name']}|{customer['contact']}\n")


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

        if self.path == "/clientes":
            name = params.get("name", [""])[0]
            contact = params.get("contact", [""])[0]

            customers = load_customers()
            new_customer = {
                "id": len(customers) + 1,
                "name": name,
                "contact": contact
            }
            save_customer(new_customer)

            self.send_response(303)
            self.send_header("Location", "/clientes")
            self.end_headers()
        else:
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

    def render_customers_html(self):
        """Gera a página de clientes"""
        customers = load_customers()

        html = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lista de Clientes</title>
            {STYLE}
        </head>
        <body>
            <h1>Clientes Cadastrados</h1>
            <form method="post" action="/clientes">
                <label>Nome:</label>
                <input type="text" name="name" required>
                <label>Contato:</label>
                <input type="text" name="contact" required>
                <button type="submit">Cadastrar Cliente</button>
            </form>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Contato</th>
                </tr>
        """
        for customer in customers:
            html += f"""
                <tr>
                    <td>{customer['id']}</td>
                    <td>{customer['name']}</td>
                    <td>{customer['contact']}</td>
                </tr>
            """
        html += """</table>
        <a href="/">Voltar para Imóveis</a>
        </body></html>"""
        return html
