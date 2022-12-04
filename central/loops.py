from servidor.server import *


def loop_response(seletor):
    while True:
        evento = seletor.select(timeout=None)
        for chave, mascara in evento:
            if chave.data is not None:
                serve_conexao(seletor=seletor, chave=chave, mascara=mascara)
            else:
                aceita_conexao(seletor=seletor, socket=chave.fileobj)
