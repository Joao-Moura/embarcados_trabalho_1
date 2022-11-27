import json
import RPi.GPIO as GPIO

from callbacks import *


def inicializa_pinos(pinos_json):
    with open(pinos_json, 'r') as f:
        pinos = json.loads(f.read())

    for pino in pinos.values():
        gpio = pino['GPIO']
        if pino['dir'] == 'in':
            GPIO.setup(gpio, GPIO.IN)
            GPIO.add_event_detect(gpio, GPIO.RISING)
        elif pino['dir'] == 'out':
            GPIO.setup(gpio, GPIO.OUT)
        elif pino['dir'] == '1-Wire':
            # TODO: Implementar 1-Wire similar ao I2C
            continue
        else:
            raise NotImplementedError(f'Direção "{pino["dir"]}" não implementada.')

    return pinos


def setta_callbacks_de_input(pinos):
    GPIO.add_event_callback(pinos['SPres']['GPIO'], callback_presenca)
    GPIO.add_event_callback(pinos['SFum']['GPIO'], callback_fumaca)
    GPIO.add_event_callback(pinos['SJan']['GPIO'], callback_janela)
    GPIO.add_event_callback(pinos['SPor']['GPIO'], callback_porta)
    GPIO.add_event_callback(pinos['SC_IN']['GPIO'], callback_entrada)
    GPIO.add_event_callback(pinos['SC_OUT']['GPIO'], callback_saida)
