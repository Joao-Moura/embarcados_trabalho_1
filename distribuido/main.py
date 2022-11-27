import sys
import RPi.GPIO as GPIO

from setup import inicializa_pinos, setta_callbacks_de_input


def main(pinos_json):
    pinos = inicializa_pinos(pinos_json=pinos_json)
    setta_callbacks_de_input(pinos=pinos)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        raise AttributeError(
            f'Chamada da função deve ser feita passando o JSON de configuração das portas.')

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    main(pinos_json=sys.argv[1])
