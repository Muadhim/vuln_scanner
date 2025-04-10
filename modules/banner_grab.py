import socket

def banner_grab(target_ip, port):
    try:
        s = socket.socket()
        s.connect((target_ip, port))
        s.send(b"HEAD / HTTP/1.1\r\n\r\n")
        banner = s.recv(1024).decode().strip()
        return banner
    except:
        return "No Banner Available"