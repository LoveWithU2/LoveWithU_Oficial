from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Inicializa a aplicação
app = Flask(__name__)
app.config.from_object(Config)

# Inicializa extensões
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# Define a rota de login padrão (usada por @login_required)
login.login_view = 'login'

# Importa as rotas e modelos depois de inicializar os objetos
from app import routes, models
