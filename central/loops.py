import json
import threading
import select
import sys

from central.server import *


def loop_response(socket):
    inputs = [sys.stdin, socket]
    sockets_distribuidos = {}

    while True:
        rlist, _, xlist = select.select(inputs, [], [])

        for read in rlist:
            if read == socket:
                nome_conexao, nova_conexao = aceita_conexao(read)
                inputs.append(nova_conexao)
                sockets_distribuidos[nome_conexao] = nova_conexao
            elif read == sys.stdin:
                conexao_enviada = callback_input(sockets_distribuidos)
                if conexao_enviada:
                    print(f'Response recebida: {trata_evento_read(conexao_enviada)}')
            else:
                print(f'Response recebida: {trata_evento_read(read)}')

        for exception in xlist:
            print(exception)
            continue
