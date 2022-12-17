import json
import csv

from types import SimpleNamespace
from datetime import datetime

from central.setup import inicializa_sala

PINOS_POSSIVEIS_OUT = [
    'L_01', 'L_02', 'AC', 'PR', 'AL_BZ',
    'alarme', 'todos', 'info', 'estado',
    'incendio'
]

SUCESSO = 'sucesso'
ERROR = 'error'


def trata_evento_read(socket):
    try:
        data_recebida = socket.recv(1024)
        return json.loads(data_recebida.decode("utf-8"))
    except (OSError, json.JSONDecodeError):
        print('Falha no recebimento, aguardando nova conexão.')


def trata_disconnect(inputs, sockets_distribuidos, socket, estado_andar):
    ip, _ = socket.getpeername()
    del estado_andar[ip]
    inputs.remove(socket)

    del sockets_distribuidos[[
        n for n, s in sockets_distribuidos.items()
        if s == socket
    ][0]]


def trata_response(response, inputs, sockets_distribuidos, estado_andar, socket):
    if not response:
        trata_disconnect(inputs, sockets_distribuidos, socket, estado_andar)
    elif response['status'] == SUCESSO:
        del response['status']
        estado_andar = altera_estado(estado_andar, socket, response)
    elif response['status'] == ERROR:
        print(response['msg'])


def altera_estado(estado_sala, socket, response):
    ip, _ = socket.getpeername()
    for gpio, valor in response.items():
        if isinstance(estado_sala[ip][gpio], dict):
            estado_sala[ip][gpio]['status'] = valor
        else:
            estado_sala[ip][gpio] = valor
    return estado_sala


def aceita_conexao(estado_andar, socket):
    conexao, addr = socket.accept()
    nome_conexao = trata_evento_read(conexao)['nome']
    estado_andar[f'{addr[0]}'] = inicializa_sala(nome_conexao)
    conexao.sendall(json.dumps({'estado': True}).encode('utf-8'))
    print(f'Conexão com nome: {nome_conexao} e addr: {addr[0]}:{addr[1]} aceita.')
    return nome_conexao, conexao


def callback_input(estado_andar, sockets_distribuidos, log):
    print(estado_andar)
    socket = input(f"Selecione o cliente. Disponíveis {list(sockets_distribuidos.keys())}")

    if socket not in sockets_distribuidos:
        print(f'Cliente "{socket}" ainda não conectou/não existe.')
        return
    
    selecionados = input(f"Ligar/desligar ({PINOS_POSSIVEIS_OUT}) [separados por ' ']: ").split()
    request = json.dumps({
        selecionado[0]: selecionado[1].lower() == "true"
        for selecionado in [s.split(':') for s in selecionados]
    })

    adiciona_log(log, socket, selecionados, request)

    try:
        sockets_distribuidos[socket].sendall(request.encode('utf-8'))
        return sockets_distribuidos[socket]
    except (ConnectionRefusedError, ConnectionResetError, OSError):
        print('Falha no envio, aguardando reconexão com servidor distribuido.')


def adiciona_log(log, sala, comando, request):
    with open(log, 'a') as f:
        arquivo = csv.writer(f, delimiter=';')
        arquivo.writerow([
            datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            sala, " ".join(comando), request
        ])
