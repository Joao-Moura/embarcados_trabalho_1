import socket


def inicializa_socket(ip, porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, porta))
    sock.listen()
    sock.setblocking(False)
    return sock
