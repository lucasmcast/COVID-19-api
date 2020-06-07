from . import api
from flask import jsonify
from datetime import date
from ..models import GeneralsDatas, CountryCases

@api.route('/all_countries', methods=["GET"])
def all_countries():
    date_now = str(date.today())
    all_data = CountryCases.query.filter_by(date_data=date_now)
    list_json = [data.to_json() for data in all_data]
    
    return jsonify(list_json), 200