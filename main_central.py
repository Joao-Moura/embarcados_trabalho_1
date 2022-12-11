import sys

from servidor.setup import inicializa_socket
from central.loops import loop_response


def main(ip, porta):
    try:
        socket = inicializa_socket(ip=ip, porta=porta)
        loop_response(socket)
    except KeyboardInterrupt:
        print('Programa Finalizado')
    finally:
        socket.close()


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        raise AttributeError(
            f'Chamada da função deve ser feita passando o ip e a porta de configuração do servidor.')

    main(ip=sys.argv[1], porta=int(sys.argv[2]))
