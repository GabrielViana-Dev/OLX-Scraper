import requests
from parsel import Selector
import json
from datetime import datetime
import csv
import time  # Import the time module


for pages in range(1, 101):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    
    r = requests.get(f'https://www.olx.com.br/imoveis/venda/estado-mg/belo-horizonte-e-regiao?o={pages}', headers=headers)

    s = Selector(text=r.text)

    html = s.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

    houses = json.loads(html)

    houses_json = houses.get('props').get('pageProps').get('ads')

    
    with open('olx_listings.csv', mode='a', newline='', encoding='utf-8') as csv_file: 
        fieldnames = ['Titulo_Anuncio', 'Link_Anuncio', 'Localizacao', 'Data_do_anuncio', 'Area_Construida', 'Quantidade_Quartos', 'Quantidade_Banheiros', 'Vagas_Garagem', 'Detalhes_Imovel', 'Detalhes_Condominio', 'Condominio_Valor', 'IPTU_Valor']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        for house_id in houses_json:
            try:
                
                titulo_anuncio = house_id["title"]
                link_anuncio = house_id["url"]
                localizacao = house_id["location"]
                data_do_anuncio = datetime.utcfromtimestamp(house_id["date"]).strftime('%d/%m/%Y %H:%M:%S')
                area_construida = next((prop["value"] for prop in house_id["properties"] if prop["name"] == "size"), None)
                quantidade_quartos = next((prop["value"] for prop in house_id["properties"] if prop["name"] == "rooms"), None)
                quantidade_banheiros = next((prop["value"] for prop in house_id["properties"] if prop["name"] == "bathrooms"), None)
                vagas_garagem = next((prop["value"] for prop in house_id["properties"] if prop["name"] == "garage_spaces"), None)
                detalhes_imovel = next((prop["value"] for prop in house_id["properties"] if prop["name"] == "re_features"), None)
                detalhes_condominio = next((prop["value"] for prop in house_id["properties"] if prop["name"] == "re_complex_features"), None)
                condominio_valor = next((prop["value"] for prop in house_id["properties"] if prop["name"] == "condominio"), None)
                iptu_valor = next((prop["value"] for prop in house_id["properties"] if prop["name"] == "iptu"), None)

                
                writer.writerow({
                    'Titulo_Anuncio': titulo_anuncio,
                    'Link_Anuncio': link_anuncio,
                    'Localizacao': localizacao,  
                    'Data_do_anuncio': data_do_anuncio,  
                    'Area_Construida': area_construida,
                    'Quantidade_Quartos': quantidade_quartos,
                    'Quantidade_Banheiros': quantidade_banheiros,
                    'Vagas_Garagem': vagas_garagem,
                    'Detalhes_Imovel': detalhes_imovel,
                    'Detalhes_Condominio': detalhes_condominio,
                    'Condominio_Valor': condominio_valor,
                    'IPTU_Valor': iptu_valor
                })

            except KeyError:
                continue

    time.sleep(5)
