from flask import Flask
#from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config

# Set Globals
#bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    """ Construindo o core da aplicação"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    
    config[config_name].init_app(app)
    #bootstrap.init_app(app)
    db.init_app(app)

    #associar rotas e paginas de erro personalizadas aqui
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app