import RPi.GPIO as GPIO

import threading

from time import sleep

from callbacks import *


PINOS_CALLBACK_IN = [
    ('SFum', callback_fumaca, 31),
    ('SJan', callback_janela, 31),
    ('SPor', callback_porta, 31),
    ('SC_IN', callback_entrada, 31),
    ('SC_OUT', callback_saida, 31),
    ('SPres', callback_presenca, 31),
]

PINOS_POSSIVEIS_OUT = ['L_01', 'L_02', 'AC', 'PR', 'AL_BZ']
PINOS_ALARME = ['SPres', 'SJan', 'SPor', 'SFum']


def loop_input(queue, pinos):
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
                    kwargs={'queue': queue, 'pinos': pinos}
                ).start()
        sleep(0.1)


def loop_output(queue, pinos):
    while True:
        selecionados = input(f"Ligar/desligar ({PINOS_POSSIVEIS_OUT}) [separados por ' ']: ").split()
        print(selecionados)

        for pino in selecionados:
            if pino in PINOS_POSSIVEIS_OUT:
                GPIO.output(pinos[pino]['GPIO'], not GPIO.input(pinos[pino]['GPIO']))
            elif pino == 'alarme':
                infos = queue.get(block=True)
                alerta_ligado = infos['sistema_alerta']

                if alerta_ligado:
                    infos['sistema_alerta'] = False
                elif not alerta_ligado and (True in [GPIO.input(pinos[p]['GPIO']) for p in PINOS_ALARME]):
                    print(f'Impossível ligar alarme se algum dos pinos {", ".join(PINOS_ALARME)} estiverem ativos.')
                else:
                    infos['sistema_alerta'] = True
                queue.put(infos)
