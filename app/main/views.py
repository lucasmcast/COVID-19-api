from flask import Flask, render_template, jsonify, request
from datetime import datetime, date
from . import main
from ..models import GeneralsDatas, CountryCases

@main.route('/', methods=['GET'])
def index():
    #pega o endereço de ip do cliente request
    ip_client = request.remote_addr
    #print é para salvar no log de acesso
    print(f"[COVID-19][INFO][index][address client] - {ip_client}")

    data_atual = date.today()
    countries_cases = CountryCases.query.filter_by(date_data=data_atual)
    generals_cases = GeneralsDatas.query.filter_by(date_data=data_atual)

    return render_template('index.html', cases=generals_cases[-1], values=countries_cases)

@main.route('/sobre', methods=["GET"])
def sobre():
    return render_template('sobre.html')

@main.route('/api-doc', methods=["GET"])
def api_doc():
    return render_template("doc.html")
