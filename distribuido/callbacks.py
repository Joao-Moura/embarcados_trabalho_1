import RPi.GPIO as GPIO

import inspect

from time import sleep

SUCESSO = 'sucesso'
ERROR = 'error'

PINOS_ALARME = ['SPres', 'SJan', 'SPor', 'SFum']
PINOS_POSSIVEIS_OUT = ['L_01', 'L_02', 'AC', 'PR', 'AL_BZ']


def callback_presenca(queue_info, queue_socket, pinos, *args, **kwargs):
    queue_socket.put({'SPres': True})
    infos = queue_info.get(block=True)
    alerta_ligado = infos['sistema_alerta']
    queue_info.put(infos)

    if alerta_ligado:
        GPIO.output(pinos['AL_BZ']['GPIO'], 1)
    else:
        luzes = [
            pinos[p]['GPIO'] for p in pinos
            if p in ('L_01', 'L_02') and not GPIO.input(pinos[p]['GPIO'])
        ]
        GPIO.output(luzes, 1)
        sleep(15)
        GPIO.output(luzes, 0)


def callback_fumaca(queue_socket, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')
    queue_socket.put({'SFum': True})


def callback_janela(queue_socket, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')
    queue_socket.put({'SJan': True})


def callback_porta(queue_socket, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')
    queue_socket.put({'SPor': True})


def callback_entrada(queue_info, *args, **kwargs):
    infos = queue_info.get(block=True)
    infos['qtd_pessoas'] += 1
    print(infos)
    queue_info.put(infos)


def callback_saida(queue_info, *args, **kwargs):
    infos = queue_info.get(block=True)
    infos['qtd_pessoas'] -= 1
    print(infos)
    queue_info.put(infos)


def callback_response(queue_info, queue_socket, response, pinos):
    for pino, status in response.items():
        if pino in PINOS_POSSIVEIS_OUT:
            GPIO.output(pinos[pino]['GPIO'], status)
            queue_socket.put({'status': SUCESSO, pino: status})
        elif pino == 'alarme':
            retorno = {}
            infos = queue_info.get(block=True)
            alerta_ligado = infos['sistema_alerta']

            if alerta_ligado:
                infos['sistema_alerta'] = status
                retorno['status'] = SUCESSO
                retorno[pino] = status
            elif not alerta_ligado and (True in [GPIO.input(pinos[p]['GPIO']) for p in PINOS_ALARME]):
                retorno['status'] = ERROR
                retorno['msg'] = f'Impossível ligar alarme se algum dos pinos {", ".join(PINOS_ALARME)} estiver ativo.'
            else:
                infos['sistema_alerta'] = status
                retorno['status'] = SUCESSO
                retorno[pino] = status
            queue_info.put(infos)
            queue_socket.put(retorno)
