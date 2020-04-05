from flask import Flask, render_template, jsonify
from datetime import datetime, date
from . import main
from ..models import GeneralsDatas, CountryCases

@main.route('/', methods=['GET'])
def index():
    data_atual = date.today()
    countries_cases = CountryCases.query.filter_by(date_data=data_atual)
    generals_cases = GeneralsDatas.query.filter_by(date_data=data_atual)

    return render_template('index.html', cases=generals_cases[-1], values=countries_cases)

@main.route('/sobre', methods=["GET"])
def sobre():
    return render_template('sobre.html')

