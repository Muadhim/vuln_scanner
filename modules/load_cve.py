import json
import os


def load_all_cve_data(folder_path):
    all_cve = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            filepath = os.path.join(folder_path, filename)

            try:
                cve = parse_cve_file(filepath)
                all_cve.append(cve)
            except Exception as e:
                print(f"Error in {filepath}: {e}")

    print(f"Total CVEs loaded: {len(all_cve)}")
    return all_cve


def parse_cve_file(file_path):
    with open(file_path, "r") as file:
        cve = json.load(file)

        product_info = []
        description = ""
        impacts = []

        cve_id = cve["cveMetadata"]["cveId"]
        container = cve["containers"]["cna"]

        for item in container.get("affected", []):
            vendor = item.get("vendor", "")
            product = item.get("product", "")
            versions = item.get("versions", [])
            version_ranges = [v.get("lessThan") for v in versions if v.get(
                "lessThan") if "lessThan" in v]
            product_info.append({
                "vendor": vendor,
                "product": product,
                "vulnerable_versions": version_ranges
            })

        for d in container.get("descriptions", []):
            if d.get("lang") == "en":
                description = d.get("value", "")
                break
        
        for i in container.get("impacts", []):
            impact_id = i.get("capecId", "")
            descriptions = [d for d in i.get("descriptions", []) if d.get("lang") == "en"]
            impacts.append({
                "capec_id": impact_id,
                "description": [d.get("value", "") for d in descriptions]
            })
        
        return {
            "cve_id": cve_id,
            "product_info": product_info,
            "description": description,
            "impacts": impacts
        }
