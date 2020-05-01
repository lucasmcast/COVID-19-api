from .country_code import get_country_code
from datetime import datetime, date
from pygal.maps.world import World

data_atual = date.today()

def get_cases(countries):
    """Delvolve os casos totais de cada pais"""
    countries_cases = countries

    cases_world = {}
    for country in countries_cases:
        name = country.country
        casos = country.total_cases
        casos = casos.replace(",", "")
        casos = int(casos)
        code = get_country_code(name)
        if code:
            cases_world[code] = casos
    
    #print(cases_world)
        
    return cases_world

def build_maps(countries):
    cases_country = get_cases(countries)
    cc_cases1, cc_cases2, cc_cases3, cc_cases4 = {}, {}, {}, {}

    for cc, cases in cases_country.items():
        if cases < 1000:
            cc_cases1[cc] = cases
        elif cases < 10000:
            cc_cases2[cc] = cases
        elif cases < 100000:
            cc_cases3[cc] = cases
        else:
            cc_cases4[cc] = cases
    
    #print(len(cc_cases1), len(cc_cases2), len(cc_cases3), len(cc_cases4))
    
    #data_str = data_atual.strftime("%d/%m/%Y")
    
    wm = World()
    wm.title = "Casos de COVID pelo Mundo"
    wm.add('1-1,000', cc_cases1)
    wm.add('1,000-10,000', cc_cases2)
    wm.add('10,000-100,000', cc_cases3)
    wm.add('>100,000', cc_cases4)

    wm.render_to_file('app/static/img/histogramas/world_cases.svg')

