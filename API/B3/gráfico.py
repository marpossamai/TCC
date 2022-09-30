from sys import displayhook
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from pandas_datareader import data as web
import numpy as np
import yahoo_finance
import matplotlib.pyplot as plt
from datetime import date

carteira = pd.read_excel('Carteira.real.xlsx')
qtde = []
nome = []
for acao in carteira['Ativos']:
    nome.append(acao)
for i in carteira['Qtde']:
    qtde.append(i)
y = np.array(qtde)
mylabels = ["Apples", "Bananas", "Cherries", "Dates"]
plt.pie(y, labels = nome)
plt.show()
