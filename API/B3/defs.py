from sys import displayhook
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from pandas_datareader import data as web
import numpy as np
import yahoo_finance
import matplotlib.pyplot as plt
from datetime import date



def procurar_acao(nome):
    ts = TimeSeries(key='2DIXCKIAIXV1A1Z9', output_format='pandas')
    return print(ts.get_symbol_search(nome))


def umanoatras():
    data_atual = date.today()
    ano = int(data_atual.year)-1
    data = data_atual.strftime(f'{ano}/%m/%d')
    return data


def mostrar_cotacao(acao):
    cotacao = web.DataReader(f'{acao}', data_source='yahoo', start=umanoatras(), end=str(date.today()))
    cot_ajustado = cotacao['Adj Close'] / cotacao['Adj Close'].iloc[0]
    retorno_cot = cot_ajustado[-1] - 1
    print(f'Retorno {acao}: {retorno_cot:.4%}')

    displayhook(cotacao)

    plt.figure(figsize=(15, 6))
    displayhook(plt.plot(cotacao['Adj Close']))
    plt.title(acao)
    plt.grid(axis='y')
    plt.show()


def ver_carteira():
    carteira = pd.read_excel('Carteira.xlsx')
    tab_acoes = {}

    for acao in carteira['Ativos']:
        cotacao = web.DataReader(acao, data_source='yahoo', start=str(date.today()), end=str(date.today()))
        tab_acoes[acao] = cotacao
        carteira.loc[carteira['Ativos'] == acao, 'Valor'] = carteira.loc[carteira['Ativos'] == acao, 'Qtde'].values * \
                                                            cotacao.loc[str(date.today()), 'Adj Close']

    dict = {}
    for acao in carteira['Ativos']:
        dict[acao] = float(carteira.loc[carteira['Ativos'] == acao, 'Valor'])

    qtde = []
    nome = []
    for i in sorted(dict, key=dict.get):
        qtde.append(dict[i])
        nome.append(i)

    y = np.array(qtde)
    x = np.array(nome)
    plt.barh(x, y)
    plt.show()

    displayhook(carteira)


def ver_tab_carteira():
    carteira = pd.read_excel('Carteira.xlsx')
    data_inicial = umanoatras()
    tab_acoes = {}

    for acao in carteira['Ativos']:
        cotacao = web.DataReader(acao, data_source='yahoo', start=umanoatras(), end=str(date.today()))
        tab_acoes[acao] = cotacao
        carteira.loc[carteira['Ativos'] == acao, 'Valor'] = carteira.loc[carteira['Ativos'] == acao, 'Qtde'].values * \
                                                            cotacao.loc[str(date.today()), 'Adj Close']

    tab_cotacoes = pd.DataFrame()
    for acao in tab_acoes:
        tab_cotacoes[acao] = tab_acoes[acao].loc[umanoatras(): str(date.today()), 'Adj Close']

    for acao in tab_cotacoes.columns:
        tab_cotacoes[acao] = tab_cotacoes[acao] * carteira.loc[carteira['Ativos'] == acao, 'Qtde'].values

    tab_cotacoes['Total'] = tab_cotacoes.sum(axis=1)
    carteira_ajustado = tab_cotacoes['Total'] / tab_cotacoes['Total'].iloc[0]  # porcentagem da carteira
    retorno_carteira = carteira_ajustado[-1] - 1
    print(f'Retorno Carteira: {retorno_carteira:.4%}')
    displayhook(tab_cotacoes)

    plt.figure(figsize=(15, 6))
    plt.subplot(2, 1, 1)
    plt.plot(tab_cotacoes['Total'])
    plt.title('Carteira')

    plt.subplot(2, 1, 2)
    plt.plot(tab_cotacoes.drop(columns=['Total']), label=carteira['Ativos'])
    plt.title('A????es da Carteira')
    plt.grid(axis='y')
    plt.legend()

    plt.show()


def comparar_cotacoes(acao1, acao2):
    cotacao1 = web.DataReader(f'{acao1}', data_source='yahoo', start=umanoatras(), end=str(date.today()))
    cotacao2 = web.DataReader(f'{acao2}', data_source='yahoo', start=umanoatras(), end=str(date.today()))

    cot1_ajustado = cotacao1['Adj Close'] / cotacao1['Adj Close'].iloc[0]
    cot2_ajustado = cotacao2['Adj Close'] / cotacao2['Adj Close'].iloc[0]

    retorno_cot1 = cot1_ajustado[-1] - 1
    retorno_cot2 = cot2_ajustado[-1] - 1

    plt.figure(figsize=(15, 6))
    plt.subplot(2, 1, 1)
    plt.plot(cotacao1['Adj Close'], color='b')
    plt.ylabel(f'Retorno: {retorno_cot1:.4%}')
    plt.title(acao1)
    plt.grid(axis='y')

    plt.subplot(2, 1, 2)
    plt.plot(cotacao2['Adj Close'])
    plt.ylabel(f'Retorno: {retorno_cot2:.4%}')
    plt.title(acao2)
    plt.grid(axis='y')
    plt.show()


def comparar_cotacao_carteira(acao1):
    carteira = pd.read_excel('Carteira.xlsx')
    data_inicial = umanoatras()

    tab_acoes = {}
    for acao in carteira['Ativos']:
        cotacao = web.DataReader(acao, data_source='yahoo', start=umanoatras(), end=str(date.today()))
        tab_acoes[acao] = cotacao
        carteira.loc[carteira['Ativos'] == acao, 'Valor'] = carteira.loc[carteira['Ativos'] == acao, 'Qtde'].values * \
                                                            cotacao.loc[str(date.today()), 'Adj Close']

    tab_cotacoes = pd.DataFrame()
    for acao in tab_acoes:
        tab_cotacoes[acao] = tab_acoes[acao].loc[umanoatras(): str(date.today()), 'Adj Close']

    for acao in tab_cotacoes.columns:
        tab_cotacoes[acao] = tab_cotacoes[acao] * carteira.loc[carteira['Ativos'] == acao, 'Qtde'].values

    tab_cotacoes['Total'] = tab_cotacoes.sum(axis=1)
    carteira_ajustado = tab_cotacoes['Total'] / tab_cotacoes['Total'].iloc[0]  # porcentagem da carteira
    retorno_carteira = carteira_ajustado[-1] - 1

    cotacao = web.DataReader(f'{acao1}', data_source='yahoo', start=umanoatras(), end=str(date.today()))
    cot_ajustado = cotacao['Adj Close'] / cotacao['Adj Close'].iloc[0]
    retorno_cot = cot_ajustado[-1] - 1

    plt.figure(figsize=(15, 6))
    plt.subplot(2, 1, 1)
    plt.plot(cotacao['Adj Close'], color='purple')
    plt.ylabel(f'Retorno: {retorno_cot:.4%}')
    plt.title(acao1)
    plt.grid(axis='y')

    plt.subplot(2, 1, 2)
    plt.plot(tab_cotacoes['Total'])
    plt.ylabel(f'Retorno: {retorno_carteira:.4%}')
    plt.title('Carteira')
    plt.grid(axis='y')
    plt.show()



# comparar_cotacao_carteira('ITUB4.SA')
# comparar_cotacoes('ITUB4.SA', 'VALE3.SA')
#ver_tab_carteira()
# ver_carteira()
# mostrar_cotacao('VALE3.SA')
# umanoatras()
# procurar_acao('ibov')