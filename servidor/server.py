import selectors
import json

from types import SimpleNamespace


def serve_conexao(seletor, chave, mascara):
    socket = chave.fileobj
    data = chave.data

    if mascara & selectors.EVENT_READ:
        data_recebida = socket.recv(1024)

        if data_recebida:
            data.entrada += data_recebida
        else:
            seletor.unregister(socket)
            socket.close()
            print(json.loads(data.entrada.decode('utf-8')))

    if mascara & selectors.EVENT_WRITE:
        ...


def aceita_conexao(seletor, socket):
    conexao, addr = socket.accept()
    print(f'Conexão {conexao} aceita')
    conexao.setblocking(False)
    data = SimpleNamespace(addr=addr, entrada=b'', saida=b'')
    seletor.register(conexao, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)
