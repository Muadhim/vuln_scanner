import re
import socket


def guest_service_from_banner(banner):
    banner = banner.strip()

    # Try to find product/version patterns like product/1.2.3 or v1.2.3
    matches = re.findall(r"([\w\-]+)[/v]?(\d+\.\d+(?:\.\d+)?)", banner)

    if matches:
        # Just take the first match
        product, version = matches[0]
        product = clean_product_name(product)
        return {
            "vendor": "Unknown",
            "product": product,
            "version": version
        }

    # Fallback; look just for a version
    version_match = re.search(r"v?(\d+\.\d+(?:\.\d+)?)", banner)
    if version_match:
        version = version_match.group(1)
        words = banner.split()

        # try to use word before version as product
        for i, word in enumerate(words):
            if version in word and i > 0:
                product = clean_product_name(words[i - 1])
                return {
                    "vendor": "Unknown",
                    "product": product,
                    "version": version
                }

    product = clean_product_name(banner.split()[0] if banner else "Unknown")
    return {
        "vendor": "Unknown",
        "product": product,
        "version": "Unknown"
    }


def clean_product_name(name):
    # Remove common special characters and parentheses
    name = re.sub(r"[^\w\-]", "", name)
    return name.strip().lower()


def banner_grab(target_ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, port))
        s.send(b"HEAD / HTTP/1.1\r\n\r\n")
        banner = s.recv(1024).decode().strip()
        return guest_service_from_banner(banner)
    except:
        return "No Banner Available"
