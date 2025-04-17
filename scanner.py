import argparse
from modules.load_cve import load_all_cve_data
from modules.port_scan import port_scan
from modules.banner_grab import banner_grab
from modules.vuln_lookup import check_vulnerabilities
from modules.report_gen import generate_report


def main():
    parser = argparse.ArgumentParser(
        description="Automated Vulnerability Scanner")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("--quick", action="store_true",
                        help="Quick scan (top 100 ports)")
    parser.add_argument("--cvepath", help="Path to CVE database")
    args = parser.parse_args()

    target = args.target
    cve_path = args.cvepath

    scan_result = {}

    cve_data = load_all_cve_data(cve_path)

    # parform port scanning
    if args.quick:
        ports = [21, 22, 80, 443, 512, 513, 514]

        for port in ports:
            if port_scan(target, port):
                banner = banner_grab(target, port)
                vuln = check_vulnerabilities(banner, cve_data)
                scan_result[port] = {"banner": banner, "vulnerability": vuln}

    # generate report
    generate_report(scan_result)


if __name__ == "__main__":
    main()
