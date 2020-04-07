from app import db
from app.models import GeneralsDatas, CountryCases
from app.get_data import ServGetData
from datetime import date, datetime
from flasky import app
from copy import deepcopy
from sqlalchemy import exc

class EnginerDB:
    
    def __init__(self):
        self.serv_getdata = ServGetData()

    
    def insert_data_cases(self):
        """
        Insere os dados no banco de dados obtidos pela web.
        Dados usados das informações gerais de casos.
        """
        #print("[INFO]: Inserindo Dados Gerais")
   
        with app.app_context():
            date_atual = datetime.now()
            hour_now = date_atual.strftime('%H:%M')
            date_now = str(date.today()).strip()

            data = self.serv_getdata.get_all_cases()
            data_db = self.get_data_db(GeneralsDatas)
            date_last_db = ''

            #Condição para validar caso o banco de dados esteje vazio
            if data_db:
                date_last_db = data_db[-1].date_data.strip()
            
            #print("Total de Dados Gerais no DB: {}".format(len(data_db)))

            #Condição para verificar se os dados obtidos são da data atual
            #Caso sejam diferentes, os dados são inseridos, de outra maneira,
            #os dados são atualizados.
            if date_last_db != date_now:
                generals_datas = GeneralsDatas(total_cases=data['total_cases'],\
                    total_deaths=data['total_deaths'], total_recovered=data['total_recovered'],\
                        date_data=date_now, hour_data=hour_now)

                try:
                    db.session.add(generals_datas)
                    db.session.commit()
                    #print("[INFO]: Dados Gerais Inseridos\n")
                except exec.SQLAlchemyError as e:
                    print("[COVID-19][WARNING][insert_data_cases] - Erro ao inserir dados gerais")
            else:
                generals_datas = data_db[-1]
                generals_datas.total_cases=data['total_cases']
                generals_datas.total_deaths=data['total_deaths'] 
                generals_datas.total_recovered=data['total_recovered']
                generals_datas.hour_data =hour_now

                try:
                    db.session.add(generals_datas)
                    db.session.commit()
                    #print("[INFO]: Dados Gerais Atualizados\n")
                except exc.SQLAlchemyError as e:
                    print("[COVID-19][WARNING][insert_data_cases] - Erro ao atualizar dados gerais")

    
    def insert_data_countries(self):
        """
        Insere os dados no banco de dados obtidos pela web.
        Dados usados da tabela de casos por paises
        """
        #print("[INFO]: Inserindo Dados por países")
        #print(app.name)
        with app.app_context():
            date_atual = datetime.now()
            hour_now = date_atual.strftime('%H:%M')
            date_now = str(date.today()).strip()
            #date_now = '2020-03-24'

            #obtem os dados da pagina web
            data = self.serv_getdata.get_countries()
            #obtem os dados do banc
            data_db = self.get_data_db(CountryCases)
            
            date_last_db = ''

            #Faz a conversão dos dados do banco,
            #para comparar com os dados da web de forma ordenada
            dataDB_converted = self.convert_dbTojson(data_db)
            
            #Ordena tambem os dados obtidos da web
            data = sorted(data, key=lambda k: k['country'])
            
            #print("Total de Paises: {}".format(len(dataDB_converted)))
            list_aux = self.compare_lists(data, dataDB_converted)

            #Condição para validar caso o banco esteje vazio.
            if data_db:
                date_last_db = data_db[-1].date_data.strip()

            country_datas = []
            
            #Condição para verificar se os dados obtidos são da data atual
            #Caso sejam diferentes, os dados são inseridos, de outra maneira,
            #os dados são atualizados.
            if date_last_db != date_now: 
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
                try:
                    db.session.add_all(country_datas)
                    db.session.commit()
                    #print("[INFO]: Dados Por Países Inseridos\n")
                except exc.SQLAlchemyError as e:
                    print("[COVID-19][WARNING][insert_data_countries] - Erro ao Inserir Paises")
            else:
                for row in list_aux:
                    data_db.append(CountryCases(
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

                for i, row in enumerate(data):
                    data_db[i].country = row['country']
                    data_db[i].url_country = row['url_country']
                    data_db[i].total_cases = row['total_cases']
                    data_db[i].new_cases = row['new_cases']
                    data_db[i].deaths_cases = row['deaths_cases']
                    data_db[i].new_deaths = row['new_deaths']
                    data_db[i].total_recovered = row['total_recovered']
                    data_db[i].active_cases = row['active_cases']
                    data_db[i].serious_critical = row['serious_critical']
                    data_db[i].hour_data = hour_now

                #print(len(data_db))
                try:
                    db.session.add_all(data_db)
                    db.session.commit()
                    #print("[INFO]: Dados Por Países Atualizados\n")
                except exc.SQLAlchemyError as e:
                    print("[COVID-19][WARNING][insert_data_countries] - Erro ao atualizar Paises")
                

     
    def get_data_db(self, models):
        """
        Função obtem os dados do banco de dados usando como
        filtro a data atual e retornando os dados.
        """   
        data = []
        data_atual = date.today()
        #data_atual = '2020-03-24'
        try:
            data = models.query.filter_by(date_data=data_atual).all()
        except exc.SQLAlchemyError as e:
            print("[COVID19][Warning][get_data_db] - Erro ao fazer busca no banco de dados")
        finally:
            return data


    
    def convert_dbTojson(self, data):
        """
        Função converte dados do banco para uma lista json,
        de forma ordenado pelo nome do país
        """
        list_data = []
        for row in data:
            list_data.append(row.to_json_noturl())

        list_data = sorted(list_data, key=lambda k: k['country'])
        return list_data
    
    
    def compare_lists(self, list_1, list_2):
        """
        Faz a comparação em a lista de dados obtida pela web e a 
        lista de dados obtida pelo banco de dados, trazendo como retorno
        os dados diferentes entre elas
        """
        list_aux = deepcopy(list_1)
        list_diferent = []
        
        for i, row in enumerate(list_1):
            #print("Primeiro Teste: [{}] {} = {}".format(i,dataDB_converted[i]['country'], row['country']))
            for j, row_db in enumerate(list_2):
                if list_1[i]['country'] == list_2[j]['country']:
                    list_aux[i]['country'] = 'Igual'
                    break

        for i, row in enumerate(list_aux):
            if row['country'] != 'Igual':
                list_diferent.append(row)

        return list_diferent