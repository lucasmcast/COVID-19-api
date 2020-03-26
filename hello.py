import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, url_for

from urllib.request import urlopen as uReq
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
from threading import Thread
from time import sleep
from datetime import date, datetime

"""
CLASSE MODELOS
"""


class ServGetData:

    def get_countries(self):
        print("[INFO]: Iniciando a busca de dados por país")
        
        my_url = "https://www.worldometers.info/coronavirus/"
        #cria uma lista vazia de paises
        countries_list = []    
        try:
            uClient = uReq(my_url)
            page_html = uClient.read()
            uClient.close()
            #converte a pagina html para o tipo BeautifulSoup
            page_soup = soup(page_html, "html.parser")
            #Busca no codigo html a tag table.
            countries_tables = page_soup.find("table")
            #constantes que indicam o indice da tabela. Parte horizontal(linha)
            COL_COUNTRY_INDEX = 0
            COL_TOTAL_CASES = 1
            COL_NEW_CASES = 2
            COL_TOTAL_DEATHS = 3
            COL_NEW_DEATHS = 4
            COL_TOTAL_RECOVERED = 5
            COL_ACTIVE_CASES = 6
            COL_SERIOUS_CRITICAL = 7
            #Obtem o numero de paises na tabela
            total_countries = (len(countries_tables.findAll('tr')) -1)
            #obtem os dados da tabela com a tag tr
            table_html = countries_tables.findAll('tr')[1:total_countries]
            #percorre a tabela obtendo os dados por linha
            for row in table_html:
                #obtem as informações da tag td
                countries = row.findAll('td')
                country = countries[COL_COUNTRY_INDEX].text.strip()
                #Nome do pais com o link de outro nivel
                url_country = countries[COL_COUNTRY_INDEX].find('a')
                if url_country:
                    url_country = url_country.get('href').strip()
                total_cases_country = countries[COL_TOTAL_CASES].text.strip()
                new_cases_country = countries[COL_NEW_CASES].text.strip()
                total_deaths_country = countries[COL_TOTAL_DEATHS].text.strip()
                new_deaths_country = countries[COL_NEW_DEATHS].text.strip()
                total_recovered_country = countries[COL_TOTAL_RECOVERED].text.strip()
                active_cases_country = countries[COL_ACTIVE_CASES].text.strip()
                serious_critical_country = countries[COL_SERIOUS_CRITICAL].text.strip()
                new_countries = {
                    'country' : country,
                    'url_country' : url_country,
                    'total_cases' : total_cases_country,
                    'new_cases' : new_cases_country,
                    'deaths_cases' : total_deaths_country,
                    'new_deaths' : new_deaths_country,
                    'total_recovered' : total_recovered_country,
                    'active_cases' : active_cases_country,
                    'serious_critical' : serious_critical_country
                }
                
                countries_list.append(new_countries)
        except HTTPError as e:
            print(e.reason, " ", e.code)
        return countries_list
    
    def get_all_cases(self):
        print("[INFO]: Iniciando a busca por dados gerais")
        total_numbers_cases = {}
        try:
            my_url = "https://www.worldometers.info/coronavirus/"
            uClient = uReq(my_url)
            page_html = uClient.read()
            uClient.close()
            page_soup = soup(page_html, "html.parser")

            #div que contem o total de casos, mortos e recuperados.
            containers = page_soup.findAll("div", {"class":"maincounter-number"})
            
            total_cases = containers[0].span.text.strip()
            total_deaths = containers[1].span.text.strip()
            total_recovered = containers[2].span.text.strip()
            total_numbers_cases = {
                'total_cases' : total_cases,
                'total_deaths' : total_deaths,
                'total_recovered' : total_recovered
            }
        except HTTPError as e:
            print(e.reason, " ", e.code)
        return total_numbers_cases

# lst_corona = get_countries()
# pint(list_corona)
# fr country in list_corona[:5]:
#    print(country)
#    print("------------")
# ttal_numbers_cases = get_all_cases()
# i len(total_numbers_cases) > 0: 
#    print("Total de Casos: {}".format(total_numbers_cases['total_cases']))
#    print("Total de Mortos: {}".format(total_numbers_cases['total_deaths']))
#    print("Total de Recuperados: {}".format(total_numbers_cases['total_recovered']))


class IntervalRunner(Thread):
    
    def __init__(self, interval, function):
        Thread.__init__(self)

        self.interval = interval
        self.function = function
        self.executing = False

    def run(self):
        self.executing = True
        while self.executing:
            self.function()
            sleep(self.interval)
    
    def stop(self):
        self.executing = False

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()


class GeneralsDatas(db.Model):
    
    __tablename__ = 'generals_datas'
    id = db.Column(db.Integer, primary_key=True)
    total_cases = db.Column(db.String(20))
    total_deaths = db.Column(db.String(20))
    total_recovered = db.Column(db.String(20))
    date_data = db.Column(db.String(20))
    hour_data = db.Column(db.String(5))

    def __repr__(self):
        return "<GeneralsDatas(total_cases='{}',\
            total_deaths='{}',total_recovered='{}', date_data='{}', hour_data='{}')>".format(self.total_cases,
            self.total_deaths, self.total_recovered, self.date_data, self.hour_data)
    
    def to_json(self):
        json_generaldata = {
            'url' : url_for('all_cases'),
            'total_cases' : self.total_cases,
            'total_deaths' : self.total_deaths,
            'total_recovered' : self.total_recovered,
            'dade_data' : self.date_data,
            'hour_data' : self.hour_data
        }

        return json_generaldata

class CountryCases(db.Model):

    __tablename__ = 'country_cases'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(20))
    url_country = db.Column(db.String(50))
    total_cases = db.Column(db.String(20))
    new_cases = db.Column(db.String(20))
    deaths_cases = db.Column(db.String(20))
    new_deaths = db.Column(db.String(20))
    total_recovered = db.Column(db.String(20))
    active_cases = db.Column(db.String(20))
    serious_critical = db.Column(db.String(20))
    date_data = db.Column(db.String(20))
    hour_data = db.Column(db.String(5))

    def __repr__(self):
        return "<CountryCases(country='{}', url_country='{}',\
            total_cases='{}', new_cases='{}',deaths_cases='{}',\
                new_deaths='{}', total_recovered='{}', actice_cases='{}',\
                    serious_critical='{}', date_data='{}', hour_data='{}')>".format(self.country,
                    self.url_country, self.total_cases,
                    self.new_cases, self.deaths_cases, self.new_deaths,
                    self.total_recovered, self.active_cases, self.serious_critical,
                    self.date_data, self.hour_data)

    def to_json(self):
        data_json = {
            'url' : url_for('all_coutries'),
            'country' : self.country,
            'url_country' : self.url_country,
            'total_cases' : self.total_cases,
            'new_cases' : self.new_cases,
            'deaths_cases' : self.deaths_cases,
            'new_deaths' : self.new_deaths,
            'total_recovered' : self.total_recovered,
            'active_cases' : self.active_cases,
            'serious_critical' : self.serious_critical,
            'date_data' : self.date_data,
            'hour_data' : self.hour_data
        }
        return data_json

class ListCountryCases:

    def __init__(self):
        self._list_country_cases = []

    def set_list_countries(self, list_countries):
        self._list_country_cases = list_countries

    def get_list_countries(self):
        return self._list_country_cases

class ListGeneralsDatas:

    def __init__(self):
        self._list_generals_datas = []

    def set_general_datals(self, list_generals_datas):
        self._list_generals_datas = list_generals_datas
    
    def get_generals_datals(self):
        return self._list_generals_datas

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app

app = create_app()
app.app_context().push()

serv_getdata = ServGetData()

def insert_data_cases():
    print("[INFO]: Inserindo Dados Gerais")
    with app.app_context():
        date_atual = datetime.now()
        hour_now = str(date_atual.hour) + ':' + str(date_atual.minute)
        date_now = str(date.today())
        data = serv_getdata.get_all_cases()
        generals_datas = GeneralsDatas(total_cases=data['total_cases'],\
            total_deaths=data['total_deaths'], total_recovered=data['total_recovered'],\
                date_data=date_now, hour_data=hour_now)
        db.session.add(generals_datas)
        db.session.commit()

def insert_data_countries():
    print("[INFO]: Inserindo Dados por país")
    
    with app.app_context():

        date_atual = datetime.now()
        hour_now = str(date_atual.hour) + ':' + str(date_atual.minute)
        date_now = str(date.today())

        data = serv_getdata.get_countries()
        country_datas = []
        print('###############',len(data))
        print(data)

        for row in data:
            country_datas.append(CountryCases(
                country = row['country'],
                url_country = row['url_country'],\
                total_cases = row['total_cases'],\
                new_cases = row['new_cases'],\
                deaths_cases = row['deaths_cases'],\
                new_deaths = row['new_deaths'],\
                total_recovered = row['total_recovered'],\
                active_cases = row['active_cases'],\
                serious_critical = row['serious_critical'],\
                date_data = date_now,\
                hour_data = hour_now
            ))
        db.session.add_all(country_datas)
        db.session.commit()

@app.route('/all_cases', methods=['GET'])
def all_cases():
    date_now = str(date.today())
    generals = GeneralsDatas.query.\
        filter_by(date_data=date_now)

    return jsonify(generals[-1].to_json()), 200



@app.route('/all_coutries', methods=['GET'])
def all_coutries():
    date_now = str(date.today())
    all_data = CountryCases.query.filter_by(date_data=date_now)
    list_json = []
    for data in all_data:
        list_json.append(data.to_json())
    print(len(list_json))
    return jsonify(list_json[105:]), 200

# interval_1 = IntervalRunner(60, insert_data_cases)
# interval_2 = IntervalRunner(60, insert_data_countries)
# interval_1.start()
# interval_2.start()

