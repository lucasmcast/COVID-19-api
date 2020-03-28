#Este modulo é o local em que está definida a instância da aplicação

import os
from flask_migrate import Migrate, upgrade
from app import create_app
from app.models import GeneralsDatas, CountryCases, db


#A configuração será obtida da variavel de ambiente FLASK_CONFIG
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()
app.config

migrate = Migrate(app, db)

from enginer_db import EnginerDB
from interval_runner import IntervalRunner

enginer = EnginerDB()

interval_allCases = IntervalRunner(60, enginer.insert_data_cases)
interval_allCountries = IntervalRunner(60, enginer.insert_data_countries)
interval_allCases.start()
interval_allCountries.start()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, GeneralsDatas=GeneralsDatas, CountryCases=CountryCases)

@app.cli.command()
def deploy():
    """Executar tarefas de implantação"""
    #Faz a migração do banco de dados para a versão mais recente
    upgrade()