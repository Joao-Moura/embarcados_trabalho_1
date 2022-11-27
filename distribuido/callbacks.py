import inspect


def callback_presenca(pino):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_fumaca(pino):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_janela(pino):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_porta(pino):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_entrada(pino):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_saida(pino):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')
