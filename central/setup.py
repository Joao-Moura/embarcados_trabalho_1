import os
import csv


def inicializa_sala(nome_sala):
    return {
        "nome_sala": nome_sala,
        "L_01": {
            "nome": "Lâmpada 1",
            "status": False
        },
        "L_02": {
            "nome": "Lâmpada 2",
            "status": False
        },
        "AC": {
            "nome": "Ar Condicionado",
            "status": False
        },
        "PR": {
            "nome": "Projetor",
            "status": False
        },
        "AL_BZ": {
            "nome": "Alarme Sonoro",
            "status": False
        },
        "SPres": {
            "nome": "Sensor de Presença",
            "status": False
        },
        "SFum": {
            "nome": "Sensor de Fumaça",
            "status": False
        },
        "SJan": {
            "nome": "Sensor de Janela",
            "status": False
        },
        "SPor": {
            "nome": "Sensor de Porta",
            "status": False
        },
        "temperatura": 0,
        "humidade": 0,
        "sistema_alerta": False,
        "sistema_incendio": False,
        "qtd_pessoas": 0
    }


def inicializa_log(nome_arquivo):
    if os.path.exists(nome_arquivo):
        return

    with open(nome_arquivo, 'w') as f:
        arquivo = csv.writer(f, delimiter=';')
        arquivo.writerow(['Data/Hora', 'Nome Sala', 'Comando Executado', 'Request Enviado'])
