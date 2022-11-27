import json
import sys
import RPi.GPIO as GPIO

from time import sleep


# def callback_example(channel):
#     print(f'botão {channel} pressionado')


# def main():
#     GPIO.setup(18, GPIO.OUT)
#     GPIO.setup(7, GPIO.IN)
#     GPIO.add_event_detect(7, GPIO.RISING)
#     GPIO.add_event_callback(7, callback_example)

#     for _ in range(10):
#         GPIO.output(18, GPIO.HIGH)
#         sleep(0.8)
#         print('acendeu')
#         GPIO.output(18, GPIO.OUT)
#         sleep(0.8)
#         print('desligou')


def inicializa_pinos(pinos_json):
    with open(pinos_json, 'r') as f:
        pinos = json.loads(f.read())

    for pino in pinos.values():
        if pino['dir'] == 'in':
            GPIO.setup(pino['GPIO'], GPIO.IN)
        elif pino['dir'] == 'out':
            GPIO.setup(pino['GPIO'], GPIO.OUT)
        elif pino['dir'] == '1-Wire':
            # TODO: Implementar 1-Wire similar ao I2C
            continue
        else:
            raise NotImplementedError(f'Direção "{pino["dir"]}" não implementada.')

    return pinos


def main(pinos_json):
    pinos = inicializa_pinos(pinos_json=pinos_json)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        raise AttributeError(f'Chamada da função deve ser feita passando o JSON de configuração das portas.')

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    main(pinos_json=sys.argv[1])
