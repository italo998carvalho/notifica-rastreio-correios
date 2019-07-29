import requests
import os
from enum import Enum
from bs4 import BeautifulSoup as bs
from cleantext import clean
from send_email.mail_sender import MailSender

codigo_de_rastreio = 'PU333550834BR'

link = 'https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm?'
data = {'objetos': codigo_de_rastreio}

source = requests.post(link, data=data)
soup = bs(source.text, 'lxml')

tabela_de_eventos = soup.find('table', class_='listEvent sro')
lista_de_eventos = tabela_de_eventos.find_all('tr')

evento = lista_de_eventos[0]
    
detalhe_evento = evento.find('td', class_='sroLbEvent')
detalhe_evento_sem_pontuacao = str(detalhe_evento.contents[1].text) + str(detalhe_evento.contents[4])
detalhe_evento_formatado = clean(detalhe_evento_sem_pontuacao)

with open('ultimo_evento.txt', 'r+') as file_:
    itens_do_arquivo = file_.readlines()

    mail_sender = MailSender(detalhe_evento_formatado, os.environ['RECEIVER_EMAIL'])

    if len(itens_do_arquivo) > 0:
        ultimo_evento = itens_do_arquivo[0]
        if ultimo_evento != detalhe_evento_formatado:
            cmd = f'sed -i "s#{ultimo_evento}#{detalhe_evento_formatado}#g" ultimo_evento.txt'
            os.system(cmd)

            mail_sender.send()
    else:
        file_.write(detalhe_evento_formatado)

        mail_sender.send()