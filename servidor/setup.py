import socket
import json

from time import sleep


def inicializa_socket(ip, porta, blocking=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(blocking)
    sock.bind((ip, porta))
    sock.listen()
    return sock


def realiza_conexao(ip, porta, nome_sala):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, porta))
            request = json.dumps({'nome': nome_sala})
            sock.sendall(request.encode('utf-8'))
            return sock
        except (ConnectionRefusedError, OSError):
            print('Não foi possível conectar, tentando novamente em 2s')
            sleep(2)
