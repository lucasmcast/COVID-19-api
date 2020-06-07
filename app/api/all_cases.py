from . import api
from flask import jsonify
from datetime import date
from ..models import GeneralsDatas, CountryCases

@api.route('/all_cases', methods=["GET"])
def all_cases():
    date_now = str(date.today())
    generals = GeneralsDatas.query.\
        filter_by(date_data=date_now)

    return jsonify(generals[-1].to_json()), 200