import json
import threading
import select
import sys

from time import sleep

from central.server import *


def loop_response(socket, log):
    inputs = [sys.stdin, socket]
    sockets_distribuidos = {}
    estado_andar = {}

    threading.Thread(target=mostra_status, args=(estado_andar, sockets_distribuidos)).start()

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


def mostra_status(estado_andar, sockets_distribuidos):
    while True:
        if not estado_andar:
            sleep(5)

        for sala in estado_andar:
            nome_sala = estado_andar[sala]["nome_sala"]
            try:
                sockets_distribuidos[nome_sala].sendall(
                    json.dumps({'estado': True}).encode('utf-8'))
            except (ConnectionRefusedError, ConnectionResetError, OSError):
                print('Falha no envio, aguardando reconexão com servidor distribuido.')
                break

            print(f'-== Estado da {nome_sala} ==-')
            for chave, valor in list(estado_andar[sala].items())[1:]:
                if isinstance(valor, dict):
                    print(f'{valor["nome"]}: {"ligado" if valor["status"] else "desligado"}')
                else:
                    print(f'{chave}: {valor}')

            print('\n')
        sleep(5)
