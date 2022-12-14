import json
import RPi.GPIO as GPIO
import Adafruit_DHT


def inicializa_placa(json_entrada):
    with open(json_entrada, 'r') as f:
        arquivo = json.loads(f.read())

    nome_sala = arquivo['nome_sala']
    ip = arquivo['ip_server']
    porta = arquivo['porta_server']
    pinos = arquivo['pinos']

    for pino in pinos.values():
        gpio = pino['GPIO']
        if pino['dir'] == 'in':
            GPIO.setup(gpio, GPIO.IN)
        elif pino['dir'] == 'out':
            GPIO.setup(gpio, GPIO.OUT)
            GPIO.output(gpio, 0)
        elif pino['dir'] == '1-Wire':
            continue
        else:
            raise NotImplementedError(f'Direção "{pino["dir"]}" não implementada.')

    return nome_sala, ip, porta, pinos
