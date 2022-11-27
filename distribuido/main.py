import sys
import RPi.GPIO as GPIO

from multiprocessing import Queue, Process

from setup import inicializa_pinos
from loops import loop_input, loop_output


def main(pinos_json):
    pinos = inicializa_pinos(pinos_json=pinos_json)
    queue_input, queue_output = Queue(), Queue()
    processo_input = Process(target=loop_input, args=(queue_input, pinos), daemon=True)
    # processo_output = Process(target=loop_output, args=(queue_output,), daemon=True)

    queue_input.put({'qtd_pessoas': 0})

    processo_input.start()
    # processo_output.start()

    processo_input.join()
    # processo_output.join()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        raise AttributeError(
            f'Chamada da função deve ser feita passando o JSON de configuração das portas.')

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    main(pinos_json=sys.argv[1])
