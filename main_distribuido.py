import sys
import RPi.GPIO as GPIO

from multiprocessing import Queue, Process

from distribuido.setup import inicializa_pinos
from distribuido.loops import loop_input, loop_output, loop_output_deprec


def main(ip, porta, pinos_json):
    pinos = inicializa_pinos(pinos_json=pinos_json)
    queue_infos, queue_socket = Queue(), Queue()
    processo_input = Process(target=loop_input, args=(queue_infos, queue_socket, pinos), daemon=True)
    processo_output = Process(target=loop_output, args=(queue_socket, ip, porta), daemon=True)

    queue_infos.put({
        'qtd_pessoas': 0,
        'sistema_alerta': False
    })

    try:
        processo_input.start()
        processo_output.start()

        loop_output_deprec(queue_infos, pinos)
        processo_input.join()
        processo_output.join()
    except KeyboardInterrupt:
        print('Programa Finalizado')
    finally:
        processo_input.join()


if __name__ == '__main__':
    if len(sys.argv) <= 3:
        raise AttributeError(
            f'Chamada da função deve ser feita passando o JSON de configuração das portas.')

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    main(ip=sys.argv[1], porta=int(sys.argv[2]), pinos_json=sys.argv[3])
