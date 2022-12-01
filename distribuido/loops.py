import RPi.GPIO as GPIO

from time import sleep

from callbacks import *


PINOS_CALLBACK_IN = [
    ('SPres', callback_presenca, 33),
    ('SFum', callback_fumaca, 31),
    ('SJan', callback_janela, 31),
    ('SPor', callback_porta, 31),
    ('SC_IN', callback_entrada, 31),
    ('SC_OUT', callback_saida, 31),
]

PINOS_POSSIVEIS_OUT = ['L_01', 'L_02', 'AC', 'PR', 'AL_BZ']


def loop_input(queue, pinos):
    for pino, _, borda in PINOS_CALLBACK_IN:
        GPIO.add_event_detect(
            pinos[pino]['GPIO'],
            borda, bouncetime=200
        )

    while True:
        for pino, callback, _ in PINOS_CALLBACK_IN:
            if GPIO.event_detected(pinos[pino]['GPIO']):
                callback(queue=queue, pino=pino, pinos=pinos)
        sleep(0.1)


def loop_output(pinos):
    while True:
        pino = input(f"Ligar/desligar ({PINOS_POSSIVEIS_OUT}): ")
        if pino in PINOS_POSSIVEIS_OUT:
            GPIO.output(pinos[pino]['GPIO'], not GPIO.input(pinos[pino]['GPIO']))
        elif pino == 'finalizar':
            break
