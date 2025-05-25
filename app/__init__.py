from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_wtf.csrf import CSRFProtect


# Inicializa a aplicação
app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'chave_secreta'
# Inicializa a proteção CSRF
csrf = CSRFProtect(app)

# Inicializa extensões
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# Define a rota de login padrão (usada por @login_required)
login.login_view = 'login'

# Importa as rotas e modelos depois de inicializar os objetos
from app import routes, models
