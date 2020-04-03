#Este modulo é o local em que está definida a instância da aplicação
import os
from dotenv import load_dotenv

#busca as variaveis de ambiente no arquivo .env e as cria
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    
import os
from flask_migrate import Migrate, upgrade
from app import create_app
from app.models import GeneralsDatas, CountryCases, db
from sqlalchemy import MetaData


#A configuração será obtida da variavel de ambiente FLASK_CONFIG
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()
app.config

migrate = Migrate(app, db)

#variavel determina o tempo em cada busca
tempo_exrc = 60

def is_tables_exist():
    """
    Função verifica se existe tabelas criadas no banco de dados
    return bool
    """
    metadata = MetaData(db.engine, reflect=True)
    tables = metadata.sorted_tables
    if len(tables) > 0:
        return True
    else:
        return False


from enginer_db import EnginerDB
from interval_runner import IntervalRunner

"""
Executar thread somente se as tabelas esterem criadas
"""
if is_tables_exist():
    """
    Função executa busca de dados e salva-os no banco de dados 
    """
    enginer = EnginerDB()

    interval_allCases = IntervalRunner(tempo_exrc, enginer.insert_data_cases)
    interval_allCountries = IntervalRunner(tempo_exrc, enginer.insert_data_countries)
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