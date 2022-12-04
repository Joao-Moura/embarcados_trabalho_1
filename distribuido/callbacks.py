import RPi.GPIO as GPIO

import inspect

from time import sleep


def callback_presenca(queue, pinos, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')
    infos = queue.get(block=True)
    alerta_ligado = infos['sistema_alerta']
    queue.put(infos)

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


def callback_fumaca(queue, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_janela(queue, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_porta(queue, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_entrada(queue, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')
    infos = queue.get(block=True)
    infos['qtd_pessoas'] += 1
    print(infos)
    queue.put(infos)


def callback_saida(queue, *args, **kwargs):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')
    infos = queue.get(block=True)
    infos['qtd_pessoas'] -= 1
    print(infos)
    queue.put(infos)
