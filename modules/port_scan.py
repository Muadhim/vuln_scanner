from scapy.all import IP, TCP, sr1


def port_scan(target_ip, port):
    pkt = IP(dst=target_ip) / TCP(dport=port, flags="S")
    resp = sr1(pkt, timeout=1, verbose=0)

    if resp and resp.haslayer(TCP) and resp.getlayer(TCP).flags == 0x12:
        print(f"Port {port} is open")
        return True

    else:
        print(f"Port {port} is closed")

    return False
