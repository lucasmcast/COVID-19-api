from flask import Flask, render_template, jsonify, request
from datetime import datetime, date, timedelta
from . import main
from ..models import GeneralsDatas, CountryCases
from .histogramas.world_cases import build_maps
from .histogramas.country_cases import build_country_maps
from pprint import pprint

@main.route('/', methods=['GET'])
def index():
    #pega o endereço de ip do cliente request
    ip_client = request.remote_addr
    #print é para salvar no log de acesso
    print(f"[COVID-19][INFO][index][address client] - {ip_client}")
    
    data_atual = date.today()
    cases, deaths, recovereds, labels = [], [], [], []
    try:
        
        result = GeneralsDatas.query.all()

        for row in result:
            total_cases = row.total_cases.replace(',', '')
            total_cases = int(total_cases)

            total_deaths = row.total_deaths.replace(',', '')
            total_deaths = int(total_deaths)

            total_recovereds = row.total_recovered.replace(',', '')
            total_recovereds = int(total_recovereds)

            cases.append(total_cases)
            deaths.append(total_deaths)
            recovereds.append(total_recovereds)
            labels.append(row.date_data)

        values = {
            'cases' : cases, 
            'deaths' : deaths, 
            'recovereds' : recovereds, 
            'labels' : labels
        }

        countries_cases = CountryCases.query.filter_by(date_data=data_atual)
        generals_cases = GeneralsDatas.query.filter_by(date_data=data_atual)
        
    except:
        date_before = datetime.today() - timedelta(days=1)
        countries_cases = CountryCases.query.filter_by(date_data=date_before)
        generals_cases = GeneralsDatas.query.filter_by(date_data=date_before)
        
    finally:
        return render_template('index.html', cases=generals_cases[-1], countries=countries_cases,
        values=values)

   

    

@main.route('/sobre', methods=["GET"])
def sobre():
    return render_template('sobre.html')

@main.route('/api-doc', methods=["GET"])
def api_doc():
    return render_template("doc.html")

@main.route('/world')
def world():
    data_atual = date.today()
    countries = CountryCases.query.filter_by(date_data=data_atual)
    build_maps(countries)
    return render_template('world_cases.html')

@main.route('/country/<name_country>')
def info_country(name_country):

    # Subtrai a data com 7 dias a menos
    today_sub_seven = datetime.today() - timedelta(days=7)
    date_str = today_sub_seven.strftime("%Y-%m-%d") #converte data para string

    # Faz um filtro obtendo somente dados do pais e datas acima do especificado
    results = CountryCases.query.filter(CountryCases.date_data >= date_str, CountryCases.country == name_country)
    #print(results)
    
    list_countries = []
    for country in results:
        list_countries.append(country)
    
    build_country_maps(list_countries)

    #URL da imagem é usado para renderizar o grafigo na pagina country.html
    url_img = 'img/histogramas/'+list_countries[-1].country+'_lastCases.svg'

    #Passando somente o ultimo registro para ser renderizado
    return render_template('country.html', country=list_countries[-1], url_img=url_img)