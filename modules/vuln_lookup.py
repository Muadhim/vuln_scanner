import json

def check_vulnerabilities(service, version):
    with open("data/cve_database.json", "r") as file:
        cve_data = json.load(file)

    for entry in cve_data:
        if service in entry["service"] and version in entry["version"]:
            return entry["cve_id"], entry["description"]

    return "No known vulnerabilities"            
        