from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, CriarMemoriaForm
from app.models import User, Memoria

@app.route('/')
@login_required
def index():
    return render_template('index.html', title='Página Inicial')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Email ou senha inválidos.')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Entrar', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Agora você pode fazer login.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Cadastrar', form=form)

@app.route('/criar_memoria', methods=['GET', 'POST'])
@login_required
def criar_memoria():
    form = CriarMemoriaForm()
    # lógica para salvar no banco de dados aqui
    return render_template('criar_memoria.html', form=form)

@app.route('/explorar_memorias')
@login_required
def explorar_memorias():
    # Aqui você busca todas as memórias do banco
    memorias = Memoria.query.order_by(Memoria.data.desc()).all()
    return render_template('explorar_memorias.html', memorias=memorias)