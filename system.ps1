if ( -Not (Test-Path "venv")) {
    py -m venv venv
}
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

. .\venv\Scripts\Activate.ps1
py -m pip install --upgrade pip

New-Item -ItemType Directory -Path "static\uploads" -Force

pip install flask
pip install ipython
pip install flask-wtf
pip install flask-sqlalchemy
pip install flask-migrate
pip install flask-login
pip install email_validator
pip install werkzeug
pip install invoke

flask db init
flask db migrate -m "users table"
flask db upgrade

flask db downgrade base


set FLASK_APP=app.py
set FLASK_DEBUG=1
flask run
