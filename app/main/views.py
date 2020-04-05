from flask import Flask, render_template, jsonify
from datetime import datetime, date
from . import main
from ..models import GeneralsDatas, CountryCases

@main.route('/', methods=['GET'])
def index():
    data_atual = date.today()
    return render_template('index.html', values=CountryCases.query.filter_by(date_data=data_atual))

@main.route('/sobre', methods=["GET"])
def sobre():
    return render_template('sobre.html')

