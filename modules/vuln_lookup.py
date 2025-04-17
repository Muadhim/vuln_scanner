import json
import re


def normalize_product_name(name):
    return re.sub(r"[^\w\-]", "", name).strip().lower()


def is_version_vulnerable(version, vulnerable_version):
    for v in vulnerable_version:
        if version == v:
            return True

    return False


def check_vulnerabilities(banner, cve_data=None):
    if not cve_data:
        with open("data/cve_database.json", "r") as file:
            cve_data = json.load(file)

    if not isinstance(banner, dict):
        return "Invalid banner format"

    banner_product = normalize_product_name(banner.get("product", ""))
    banner_version = banner.get("version", "")

    for entry in cve_data:
        for p in entry.get("product_info", []):
            cve_product = normalize_product_name(p.get("product", ""))
            if (cve_product == banner_product and
                    is_version_vulnerable(banner_version, p["vulnerable_versions"])):
                return {
                    "cve_id": entry["cve_id"],
                    "description": entry["description"],
                }

    return "No known vulnerabilities"
