import json
from django.shortcuts import render
import calendar
from datetime import date
import pandas as pd
import numpy as np
import csv

def index(request):
    ano = date.today().year
    mes = date.today().month
    dia = date.today().day
    dataHoje = str(date.today())
    # data = calendar.TextCalendar(calendar.SUNDAY)

    dia_semana = calendar.weekday(ano, mes, dia) #atualizar na sexta / dia da semana retorna seg==0,ter==1,qua==2,qui==3,sex==4, sab==5,DO==6
    
    nomes = np.loadtxt(fname = "nomes.txt", dtype=str)
    # se for sexta e a data da ultima atualizaçã 'nome[0] for diferente de hoje'
    if dia_semana == 4 and nomes[0] != dataHoje: ## nome[0] quarda a data da ultima atualização //data precisa ser diferente para atualizar uma vez no dia escolhido -> 'Sexta' // apos isso a data passa á ser igual impedindo atualizar ate a proxima sexta.
        n = nomes[6]
        nomes = np.delete(nomes,(6),axis=0)
        nomes = np.insert(nomes, 1, n)
        nomes = nomes.tolist()
        arquivo = open('nomes.txt', 'w')
        for x in range(7):
            lista=nomes[x]
            arquivo.write(lista+"\n")
        
        with open('listapaes.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # spamwriter.writerow(['Lista de Quem Traz Paes'])
            spamwriter.writerow(['Segunda','Terca','Quarta','Quinta','Sexta'])
            spamwriter.writerow(nomes[1:6])
            
        df = pd.read_csv('listapaes.csv', sep = ';')
        json_records = df.reset_index().to_json(orient ='records')
        data=[]
        data = json.loads(json_records)
        context = {'d': data}
        arquivo.close()
        return render(request, 'index.html', context)
    else:
        df = pd.read_csv('listapaes.csv', sep = ';')
        json_records = df.reset_index().to_json(orient ='records')
        data=[]
        data = json.loads(json_records)
        context = {'d': data}
        return render(request, 'index.html', context)
    


