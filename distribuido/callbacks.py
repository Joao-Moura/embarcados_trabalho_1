import RPi.GPIO as GPIO
import Adafruit_DHT

import inspect

from time import sleep

SUCESSO = 'sucesso'
ERROR = 'error'

PINOS_ALARME = ['SPres', 'SJan', 'SPor', 'SFum']
PINOS_TODOS = ['L_01', 'L_02', 'AC', 'PR']
PINOS_POSSIVEIS_OUT = ['L_01', 'L_02', 'AC', 'PR', 'AL_BZ']


def callback_dht22(queue_info, queue_socket, pinos, *args, **kwargs):
    while True:
        humidade, temperatura = Adafruit_DHT.read_retry(22, pinos['DHT22']['GPIO'])
        infos = queue_info.get(block=True)
        infos['temperatura'] = temperatura
        infos['humidade'] = humidade
        queue_info.put(infos)
        sleep(2)


def callback_presenca(queue_info, queue_socket, pinos, pino, *args, **kwargs):
    if not GPIO.input(pinos[pino]['GPIO']):
        queue_socket.put({'status': SUCESSO, 'SPres': False})
        return

    response = {'status': SUCESSO, 'SPres': True}
    infos = queue_info.get(block=True)
    alerta_ligado = infos['sistema_alerta']
    queue_info.put(infos)

    if alerta_ligado:
        GPIO.output(pinos['AL_BZ']['GPIO'], 1)
        response['AL_BZ'] = True
        queue_socket.put(response)
    else:
        luzes = [
            p for p in pinos
            if p in ('L_01', 'L_02') and not GPIO.input(pinos[p]['GPIO'])
        ]

        GPIO.output([pinos[l]['GPIO'] for l in luzes], 1)
        queue_socket.put(response | {p: True for p in luzes})

        sleep(15)
        GPIO.output([pinos[l]['GPIO'] for l in luzes], 0)
        queue_socket.put({'status': SUCESSO} | {p: False for p in luzes})


def callback_fumaca(queue_info, queue_socket, pinos, pino, *args, **kwargs):
    infos = queue_info.get(block=True)
    alerta_ligado = infos['sistema_incendio']
    queue_info.put(infos)

    estado = GPIO.input(pinos[pino]['GPIO'])
    response = {'status': SUCESSO}

    if estado and alerta_ligado:
        GPIO.output(pinos['AL_BZ']['GPIO'], True)
        response['AL_BZ'] = True

    queue_socket.put(response | {'SFum': bool(estado)})


def callback_janela(queue_socket, pinos, pino, *args, **kwargs):
    queue_socket.put({
        'status': SUCESSO,
        'SJan': bool(GPIO.input(pinos[pino]['GPIO']))
    })


def callback_porta(queue_socket, pinos, pino, *args, **kwargs):
    queue_socket.put({
        'status': SUCESSO,
        'SPor': bool(GPIO.input(pinos[pino]['GPIO']))
    })


def callback_entrada(queue_info, queue_socket, *args, **kwargs):
    infos = queue_info.get(block=True)
    infos['qtd_pessoas'] += 1
    queue_info.put(infos)
    queue_socket.put({
        'status': SUCESSO,
        'qtd_pessoas': infos['qtd_pessoas']
    })


def callback_saida(queue_info, queue_socket, *args, **kwargs):
    infos = queue_info.get(block=True)
    infos['qtd_pessoas'] -= 1
    queue_info.put(infos)
    queue_socket.put({
        'status': SUCESSO,
        'qtd_pessoas': infos['qtd_pessoas']
    })


def callback_response(queue_info, queue_socket, response, pinos):
    for pino, status in response.items():
        if pino in PINOS_POSSIVEIS_OUT:
            GPIO.output(pinos[pino]['GPIO'], status)
            queue_socket.put({'status': SUCESSO, pino: status})
        elif pino == 'todos':
            response = {'status': SUCESSO}
            for p in PINOS_TODOS:
                GPIO.output(pinos[p]['GPIO'], status)
                response[p] = status
            queue_socket.put(response)
        elif pino == 'info':
            infos = queue_info.get(block=True)
            queue_info.put(infos)
            queue_socket.put({'status': SUCESSO, **infos})
        elif pino == 'estado':
            response = {'status': SUCESSO}
            for p in list(pinos.keys())[:-3]:
                response[p] = bool(GPIO.input(pinos[p]['GPIO']))
            infos = queue_info.get(block=True)
            queue_info.put(infos)
            queue_socket.put(response | infos)
        elif pino == 'incendio':
            infos = queue_info.get(block=True)
            infos['sistema_incendio'] = status
            queue_info.put(infos)
            queue_socket.put({'status': SUCESSO, 'sistema_incendio': status})
        elif pino == 'alarme':
            retorno = {}
            infos = queue_info.get(block=True)
            alerta_ligado = infos['sistema_alerta']

            if not alerta_ligado and (True in [GPIO.input(pinos[p]['GPIO']) for p in PINOS_ALARME]):
                retorno['status'] = ERROR
                retorno['msg'] = f'Impossível ligar alarme se algum dos pinos {", ".join(PINOS_ALARME)} estiver ativo.'
            else:
                infos['sistema_alerta'] = status
                retorno['status'] = SUCESSO
                retorno['sistema_alerta'] = status
            queue_info.put(infos)
            queue_socket.put(retorno)
