from flask import Flask, render_template, jsonify
from datetime import datetime, date
from . import main
from ..models import GeneralsDatas, CountryCases

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    

