import json
import RPi.GPIO as GPIO


def inicializa_pinos(pinos_json):
    with open(pinos_json, 'r') as f:
        pinos = json.loads(f.read())

    for pino in pinos.values():
        gpio = pino['GPIO']
        if pino['dir'] == 'in':
            GPIO.setup(gpio, GPIO.IN)
        elif pino['dir'] == 'out':
            GPIO.setup(gpio, GPIO.OUT)
        elif pino['dir'] == '1-Wire':
            # TODO: Implementar 1-Wire similar ao I2C
            continue
        else:
            raise NotImplementedError(f'Direção "{pino["dir"]}" não implementada.')

    return pinos
