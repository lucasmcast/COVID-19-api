from pygal.maps.world import COUNTRIES

#Dicionario contendo o nome do pais que é diferente das informações obtidas via webscraping
DATA_API_COUNTRIES = {
    'USA' : 'United States',
    'UK' : 'United Kingdom',
    'Russia' : 'Russian Federation',
    'Bolivia' : 'Bolivia, Plurinational State of',
    'Venezuela' : 'Venezuela, Bolivarian Republic of',
    'Iran' : 'Iran, Islamic Republic of',
    'Libya' : 'Libyan Arab Jamahiriya',
    'Tanzania' : 'Tanzania, United Republic of',
    'DRC' : 'Congo, the Democratic Republic of the',
    'CAR' : 'Central African Republic',
    'Syria' : 'Syrian Arab Republic',
    'S. Korea' : 'Korea, Republic of',
    'Vietnam' : 'Viet Nam',
    'Laos' : 'Lao People’s Democratic Republic',
    'Czechia' : 'Czech Republic'
}
def get_country_code(country_name):
    """Devolve o codigo de duas letras do pygal para o pais, dado seu nome"""
    
    if get_country(country_name):
        country_name = get_country(country_name)

    country_name = country_name.title()
    for code, name in COUNTRIES.items():
        name = name.title()
        if name == country_name:
            return code
    # Se o pais não foi encontrado, devolve None
    return None

def get_country(country_name):
    """Devolve o pais conforme a documentação do pygal.maps"""
    try:
        return DATA_API_COUNTRIES[country_name]
    except:
        return None