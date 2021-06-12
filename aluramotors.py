import re
import json
import requests
from bs4 import BeautifulSoup

carros = {}
patual = 1

while True:
    res = requests.get(f'https://alura-site-scraping.herokuapp.com/index.php?page={patual}')
    soup = BeautifulSoup(res.text, 'html.parser')

    for card in soup.findAll('div', class_='well card'):
        nome = card.find('p', class_='txt-name inline').text
        preco = float(card.find('p', class_='txt-value').text[3:].replace('.', ''))
        # print(f'{price:.2f}'.replace('.', ','))
        motor = card.find('p', class_='txt-motor').text
        status = card.find('p', class_='txt-category badge badge-secondary inline').text
        infos = card.find('p', class_='txt-description').text.replace('.', '')
        ano, km = map(int, re.findall(r'\d+', infos))
        itens = []
        for item in card.findAll('li', class_='txt-items')[:-1]:
            itens.append(item.text[2:])
        carros[nome] = {'preco': preco, 'ano': ano, 'km': km, 'motor': motor, 'status': status, 'descricao': itens}

    paginacao = soup.find('span', class_='info-pages').text
    patual, pfinal = map(int, re.findall(r'\d+', paginacao))
    if patual == pfinal:
        break
    patual += 1

# Escreve os dados da variável carros em um arquivo JSON
with open('carros.json', 'w', encoding='utf-8') as arquivo:
    arquivo.write(json.dumps(carros, indent=2, ensure_ascii=False))
