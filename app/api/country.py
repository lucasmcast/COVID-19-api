from . import api
from flask import jsonify
from ..models import CountryCases

@api.route('/country/<name>', methods= ['GET'])
def country(name):
    #busca o pais ordenando pela data de forma decrescente
    country = CountryCases.query.filter_by(country=name)\
        .order_by(CountryCases.date_data.desc()).first_or_404()
    country_json = country.to_json()
    return jsonify(country_json)