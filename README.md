# Trabalho 1 FSE (2022-2)

## Executando o programa

1. Preencha corretamente o arquivo exemplo_pinos.json com as portas, nome do cliente, ip e portas do servidor central

```json
{
    "nome_sala": "Nome exemplo",
    "ip_server": "127.0.0.1",
    "porta_server": 1337,
    "pinos": {
        "L_01": {
            "GPIO": "Porta exemplo",
            "dir": "in, out ou 1-Wire"
        },
    ...
    }
}
```

2. Execute o servidor central ou os clientes distribuidos (não precisam ser iniciados na mesma ordem)

```sh
# Comando para inicialização do servidor central
$ python main_central.py [ip] [porta] [arquivo de saida para logs CSV]

# Comando para inicialização do cliente distribuido
$ python main_distribuido.py [arquivo de configuração JSON]
```

## Usando comandos

Inicialmente é necessário escolher para qual sala o comando será enviado. Assim que um cliente distribuido conectar, a mensagem 
`Conexão com nome: [Nome Sala] e addr: [IP Sala] aceita.` será mostrada no terminal e a partir dai a sala já estará disponível 
para receber comandos.

Portanto, basta digitar o nome da sala e a seguinte lista de comandos será exibida:
- Comandos **L_01**, **L_02**, **AC**, **PR**, **AL_BZ** ligam/desligam os seus respectivos leds.
- Comando **alarme** ativa/desativa o alarme de presença
- Comando **incendio** ativa/desativa o alarme de incêndio
- Comando **todos** liga/desliga os seguintes leds [L_01, L_02, AC, PR]
- Comando **info** atualiza as seguintes informações [temperatura, pressão, quantidade de pessoas, estado do alerta de presença e estado do alerta de fumaça]
- Comando **estado** atualiza o estado de todos os pinos + infos da sala

## Tratamento de desconexões

Caso o servidor central os clientes distribuidos se desconectem, algumas medidas são tomadas
- Servidor central off: Assim que o cliente distribuido precisar enviar uma nova informação para o servidor central, a conexão irá falhar e a partir desse momento o cliente entra em um estado de loop 
assíncrono tentando reconectar. Assim que possível a reconexão, o cliente enviará tanto o nome da sala como seu estado atual (comando **estado**).
- Cliente distribuido off: Caso o cliente se desconecte as informações de estado no servidor central referentes aquele cliente serão apagadas e assim que
acontecer a reconexão, o cliente distribuido será resetado.
