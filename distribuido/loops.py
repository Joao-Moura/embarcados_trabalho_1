import RPi.GPIO as GPIO

import threading
import socket
import json

from time import sleep
from multiprocessing import Process

from servidor.setup import *
from distribuido.callbacks import *


PINOS_CALLBACK_IN = [
    ('SFum', callback_fumaca, 33),
    ('SJan', callback_janela, 33),
    ('SPor', callback_porta, 33),
    ('SC_IN', callback_entrada, 31),
    ('SC_OUT', callback_saida, 31),
    ('SPres', callback_presenca, 33),
]

PINOS_POSSIVEIS_OUT = ['L_01', 'L_02', 'AC', 'PR', 'AL_BZ']
PINOS_ALARME = ['SPres', 'SJan', 'SPor', 'SFum']


def loop_input(queue_info, queue_socket, pinos):
    threading.Thread(
        target=callback_dht22, daemon=True,
        kwargs={
            'queue_info': queue_info,
            'queue_socket': queue_socket,
            'pinos': pinos
        }
    ).start()

    for pino, _, borda in PINOS_CALLBACK_IN:
        GPIO.add_event_detect(
            pinos[pino]['GPIO'],
            borda, bouncetime=200
        )

    while True:
        for pino, callback, _ in PINOS_CALLBACK_IN:
            if GPIO.event_detected(pinos[pino]['GPIO']):
                threading.Thread(
                    target=callback, daemon=True,
                    kwargs={
                        'queue_info': queue_info,
                        'queue_socket': queue_socket,
                        'pinos': pinos, 'pino': pino
                    }
                ).start()
        sleep(0.1)


def loop_output(queue_info, queue_socket, ip, porta, nome_sala, pinos):
    sock = realiza_conexao(ip, porta, nome_sala)
    output = inicia_output(queue_info, queue_socket, sock, pinos)

    while True:
        try:
            request = json.dumps(queue_socket.get(block=True))
            sock.sendall(request.encode('utf-8'))
        except (ConnectionRefusedError, ConnectionResetError, OSError):
            output.terminate()
            sock = realiza_conexao(ip, porta, nome_sala)
            output = inicia_output(queue_info, queue_socket, sock, pinos)


def inicia_output(queue_info, queue_socket, sock, pinos):
    output = Process(
        target=loop_output_recebe, daemon=True,
        kwargs={
            'queue_info': queue_info,
            'queue_socket': queue_socket,
            'sock': sock, 'pinos': pinos
        }
    )

    output.start()
    return output


def loop_output_recebe(queue_info, queue_socket, sock, pinos):
    while True:
        try:
            data_recebida = sock.recv(1024)
            response = json.loads(data_recebida.decode('utf-8'))

            print(f'Response recebida: {response}')
            status = callback_response(queue_info, queue_socket, response, pinos)
        except (OSError, json.JSONDecodeError):
            return
