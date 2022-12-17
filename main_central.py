import sys

from servidor.setup import inicializa_socket
from central.setup import inicializa_log
from central.loops import loop_response


def main(ip, porta, nome_arquivo):
    try:
        socket = inicializa_socket(ip=ip, porta=porta)
        inicializa_log(nome_arquivo)
        loop_response(socket, nome_arquivo)
    except KeyboardInterrupt:
        print('Programa Finalizado')
    finally:
        socket.close()


if __name__ == '__main__':
    if len(sys.argv) <= 3:
        raise AttributeError(
            f'Chamada da função deve ser feita passando o ip e a porta de configuração do servidor.')

    main(ip=sys.argv[1], porta=int(sys.argv[2]), nome_arquivo=sys.argv[3])
