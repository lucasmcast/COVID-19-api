import pygal

def build_country_maps(list_country):

    date_list= []
    cases_list = []
    for country in list_country:
        casos = country.total_cases
        casos = casos.replace(",", "")
        casos = int(casos)
        date_list.append(country.date_data)
        cases_list.append(casos)
    
    #print(date_list)
    #print(cases_list)

    # Visualizar os dados
    hist = pygal.Bar()

    hist.title = "Casos nos ultimos 7 dias"
    hist.x_labels = date_list
    hist.x_title = "Datas"
    hist.y_title = "Numero de Casos"

    hist.add("Casos", cases_list)
    hist.render_to_file("app/static/img/histogramas/"+list_country[-1].country+"_lastCases.svg")

