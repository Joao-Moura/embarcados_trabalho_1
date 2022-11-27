import RPi.GPIO as GPIO

from time import sleep

from callbacks import *


PINOS_CALLBACK_IN = [
    ('SPres', callback_presenca),
    ('SFum', callback_fumaca),
    ('SJan', callback_janela),
    ('SPor', callback_porta),
    ('SC_IN', callback_entrada),
    ('SC_OUT', callback_saida),
]


def loop_input(queue, pinos):
    for pino, _ in PINOS_CALLBACK_IN:
        GPIO.add_event_detect(pinos[pino]['GPIO'], GPIO.RISING)

    while True:
        for pino, callback in PINOS_CALLBACK_IN:
            if GPIO.event_detected(pinos[pino]['GPIO']):
                callback(queue)
        sleep(0.1)


def loop_output(queue, pinos):
    ...
