import json

from types import SimpleNamespace

PINOS_POSSIVEIS_OUT = ['L_01', 'L_02', 'AC', 'PR', 'AL_BZ', 'alarme']


def trata_evento_read(socket):
    try:
        data_recebida = socket.recv(1024)
        if data_recebida == b'ping':
            return 'PING recebido'
        return json.loads(data_recebida.decode("utf-8"))
    except (OSError, json.JSONDecodeError):
        print('Falha no recebimento, aguardando nova conexão.')


def aceita_conexao(socket):
    conexao, addr = socket.accept()
    nome_conexao = trata_evento_read(conexao)['nome']
    print(f'Conexão com nome: {nome_conexao} e addr: {addr[0]}:{addr[1]} aceita.')
    return nome_conexao, conexao


def callback_input(sockets_distribuidos):
    socket = input(f"Selecione o cliente. Disponíveis {sockets_distribuidos.keys()}")

    if socket not in sockets_distribuidos:
        print(f'Cliente "{socket}" ainda não conectou/não existe.')
        return
    
    selecionados = input(f"Ligar/desligar ({PINOS_POSSIVEIS_OUT}) [separados por ' ']: ").split()
    request = json.dumps({
        selecionado[0]: selecionado[1].lower() == "true"
        for selecionado in [s.split(':') for s in selecionados]
    })

    print(f'Request montado: {request}')
    try:
        sockets_distribuidos[socket].sendall(request.encode('utf-8'))
        return sockets_distribuidos[socket]
    except (ConnectionRefusedError, ConnectionResetError, OSError):
        print('Falha no envio, aguardando reconexão com servidor distribuido.')
