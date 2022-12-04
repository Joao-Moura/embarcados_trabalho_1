import RPi.GPIO as GPIO

import inspect

from time import sleep


def callback_presenca(queue_info, pinos, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')
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


def callback_janela(queue_info, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_porta(queue_info, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_entrada(queue_info, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')
    infos = queue_info.get(block=True)
    infos['qtd_pessoas'] += 1
    print(infos)
    queue_info.put(infos)


def callback_saida(queue_info, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')
    infos = queue_info.get(block=True)
    infos['qtd_pessoas'] -= 1
    print(infos)
    queue_info.put(infos)
