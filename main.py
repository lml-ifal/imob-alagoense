import json
import os

DATA_FILE = "imobiliaria.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"properties": [], "customers": [], "contracts": []}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Properties

# CREATE


def add_property():
    data = load_data()

    address = input("Endereço: ")
    budget = float(input("Valor: "))
    status = input("Status (disponível/alugado/vendido): ")
    owner = input("Proprietário: ")

    property = {
        "id": len(data["properties"]) + 1,
        "address": address,
        "budget": budget,
        "status": status,
        "owner": owner
    }

    data["properties"].append(property)
    save_data(data)
    print("✅ Imóvel cadastrado com sucesso!\n")


# READ
def list_properties():
    data = load_data()

    available_properties = [
        prop for prop in data["properties"] if prop["status"] == "disponível"]
    sold_properties = [prop for prop in data["properties"]
                       if prop["status"] == "vendido"]
    rented_properties = [
        prop for prop in data["properties"] if prop["status"] == "alugado"]

    if available_properties:
        print("\n📌 Imóveis disponíveis:")
        for property in available_properties:
            print(
                f"ID: {property['id']} - Endereço: {property['address']} - ${property['budget']}")
    else:
        print("\n❌ Nenhum imóvel disponível.")

    if sold_properties:
        print("\n📌 Imóveis vendidos:")
        for property in sold_properties:
            print(
                f"ID: {property['id']} - Endereço: {property['address']} - ${property['budget']}")
    else:
        print("\n❌ Nenhum imóvel vendido.")

    if rented_properties:
        print("\n📌 Imóveis alugados:")
        for property in rented_properties:
            print(
                f"ID: {property['id']} - Endereço: {property['address']} - ${property['budget']}")
    else:
        print("\n❌ Nenhum imóvel alugado.")

    print("\n")


def menu():
    while True:
        print("\n=== SISTEMA IMOBILIÁRIO ===")
        print("1. Cadastrar Imóvel")
        print("2. Listar Imóveis Disponíveis")
        print("3. Sair")

        option = input("Escolha uma opção: ")

        match option:
            case "1":
                add_property()
            case "2":
                list_properties()
            case "3":
                print("Saindo...")
                break
            case _:
                print("❌ Opção inválida. Tente novamente.")


menu()
