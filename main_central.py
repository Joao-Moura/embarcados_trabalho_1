import selectors
import sys

from central.setup import inicializa_socket
from central.loops import loop_response


def main(ip, porta):
    seletor = selectors.DefaultSelector()
    socket = inicializa_socket(ip=ip, porta=porta)
    seletor.register(socket, selectors.EVENT_READ, data=None)

    try:
        loop_response(seletor=seletor)
    except KeyboardInterrupt:
        print('Programa Finalizado')
    finally:
        seletor.close()


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        raise AttributeError(
            f'Chamada da função deve ser feita passando o ip e a porta de configuração do servidor.')

    main(ip=sys.argv[1], porta=int(sys.argv[2]))
