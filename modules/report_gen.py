import json

def generate_report(result, output_file="report.json"):
    with open(output_file, "w") as file:
        json.dump(result, file, indent=4)
    print(f"Report seved as {output_file}")