import json

dataset = []

name = input("Company Name: ")

while name != "|":
    country = input("Company Country: ")
    dataset.append({"name": name, "country": country, "suppliers": []})

    supplier = input("Supplier Name: ")
    while supplier != "`":
        supplierCountry = input("Supplier Country: ")
        dataset[-1]["suppliers"].append({"name": supplier, "country": supplierCountry})

        supplier = input("Supplier Name: ")

    name = input("Company Name: ")

with open("res.json", "a") as file:
    file.write("\n\n///////////////////////////////////////////////////////////////////////\n\n")
    json.dump(dataset, file, indent=4)
    file.write("\n\n///////////////////////////////////////////////////////////////////////\n\n")