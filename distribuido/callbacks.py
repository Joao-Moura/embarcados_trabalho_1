import inspect


def callback_presenca(queue):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_fumaca(queue):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_janela(queue):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_porta(queue):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')


def callback_entrada(queue):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')
    infos = queue.get(block=True)
    infos['qtd_pessoas'] += 1
    print(infos)
    queue.put(infos)


def callback_saida(queue):
    print(f'Função {inspect.currentframe().f_code.co_name} chamada')
    infos = queue.get(block=True)
    infos['qtd_pessoas'] -= 1
    print(infos)
    queue.put(infos)
