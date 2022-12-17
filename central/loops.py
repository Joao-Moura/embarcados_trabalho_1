import json
import threading
import select
import sys

from central.server import *


def loop_response(socket, log):
    inputs = [sys.stdin, socket]
    sockets_distribuidos = {}
    estado_andar = {}

    while True:
        rlist, wlist, xlist = select.select(inputs, [], [])

        for read in rlist:
            if read == socket:
                nome_conexao, nova_conexao = aceita_conexao(estado_andar, read)
                inputs.append(nova_conexao)
                sockets_distribuidos[nome_conexao] = nova_conexao
            elif read == sys.stdin:
                conexao_enviada = callback_input(estado_andar, sockets_distribuidos, log)
                if conexao_enviada:
                    response = trata_evento_read(conexao_enviada)
                    trata_response(response, inputs, sockets_distribuidos, estado_andar, conexao_enviada)
            else:
                response = trata_evento_read(read)
                trata_response(response, inputs, sockets_distribuidos, estado_andar, read)
