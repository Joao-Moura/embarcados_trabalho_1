import sys
import RPi.GPIO as GPIO

from multiprocessing import Queue, Process

from distribuido.setup import inicializa_placa
from distribuido.loops import loop_input, loop_output


def main(json_entrada):
    nome_sala, ip, porta, pinos = inicializa_placa(json_entrada=json_entrada)
    queue_infos, queue_socket = Queue(), Queue()
    
    processo_input = Process(
        target=loop_input, args=(queue_infos, queue_socket, pinos), daemon=True)

    processo_output = Process(
        target=loop_output, args=(
            queue_infos, queue_socket, ip,
            porta, nome_sala, pinos
        ), daemon=False
    )

    queue_infos.put({
        'qtd_pessoas': 0,
        'sistema_alerta': False,
        'temperatura': 0,
        'humidade': 0
    })

    processo_input.start()
    processo_output.start()

    processo_input.join()
    processo_output.join()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        raise AttributeError(
            f'Chamada da função deve ser feita passando o JSON de configuração das portas.')

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    main(json_entrada=sys.argv[1])
