__autor__ = "Lucas Martins de Castro"

from urllib.request import urlopen as uReq, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup

class ServGetData:

    def get_countries(self):
        print("[INFO]: Iniciando a busca de dados por país")

        #Usar um User-Agent para o site não bloquear nossa requisição
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
        }

        my_url = "https://www.worldometers.info/coronavirus/"
        req = Request(url=my_url, headers=headers)
        
        #cria uma lista vazia de paises
        countries_list = []    
        try:
            uClient = uReq(req)
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
        finally:
            return countries_list
    
    def get_all_cases(self):
        print("[INFO]: Iniciando a busca por dados gerais")
        total_numbers_cases = {}
        #Usar um User-Agent para o site não bloquear nossa requisição
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
        }

        my_url = "https://www.worldometers.info/coronavirus/"
        req = Request(url=my_url, headers=headers)

        try:
            uClient = uReq(req)
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
        finally:
            return total_numbers_cases

data = ServGetData().get_all_cases()
