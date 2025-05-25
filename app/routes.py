from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, csrf
from app.forms import LoginForm, RegistrationForm, CriarMemoriaForm, EditarPerfilForm
from app.models import User, Memoria
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from datetime import datetime, timezone


@app.route('/')
@login_required
def index():
    # Página principal após login - tipo dashboard ou área restrita
    return render_template('index.html', title='Página Inicial')

@app.route('/home')
def home():
    # Página pública acessível por qualquer usuário, logado ou não
    return render_template('home.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Email ou senha inválidos.', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))  # Redireciona para index após login
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
        flash('Cadastro realizado com sucesso! Agora você pode fazer login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Cadastrar', form=form)

@app.route('/criar_memoria', methods=['GET', 'POST'])
@login_required
def criar_memoria():
    form = CriarMemoriaForm()
    if form.validate_on_submit():
        filename = None
        if form.imagem.data:
            upload_dir = os.path.join(app.root_path, 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            filename = secure_filename(form.imagem.data.filename)
            caminho = os.path.join(upload_dir, filename)
            form.imagem.data.save(caminho)

        nova_memoria = Memoria(
            titulo=form.titulo.data,
            data=form.data.data,
            categoria=form.categoria.data,
            descricao=form.descricao.data,
            imagem=filename,
            user_id=current_user.id
        )
        db.session.add(nova_memoria)
        db.session.commit()
        return redirect(url_for('explorar_memorias'))
    return render_template('criar_memoria.html', form=form)

@app.route('/explorar_memorias')
@login_required
def explorar_memorias():
    memorias = Memoria.query.filter_by(user_id=current_user.id).order_by(Memoria.data.desc()).all()
    return render_template('explorar_memorias.html', memorias=memorias)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'uploads'), filename)

@csrf.exempt
@app.route('/deletar_memoria/<int:id>', methods=['POST'])
@login_required
def deletar_memoria(id):
    memoria = Memoria.query.get_or_404(id)
    if memoria.user_id != current_user.id:
        abort(403)
    if memoria.imagem:
        try:
            os.remove(os.path.join(app.root_path, 'static', 'uploads', memoria.imagem))
        except FileNotFoundError:
            pass
    db.session.delete(memoria)
    db.session.commit()
    flash('Memória deletada com sucesso!', 'success')
    return redirect(url_for('explorar_memorias'))


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/perfil/<username>')
@login_required
def user(username):
    user = db.first_or_404(db.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Exemplo de post 1'},
        {'author': user, 'body': 'Exemplo de post 2'},
    ]
    return render_template('perfil.html', user=user, posts=posts)

@app.route('/editar_perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = EditarPerfilForm()

    if form.validate_on_submit():
        current_user.name = form.nome.data
        current_user.cidade_estado = form.cidade_estado.data
        current_user.tempo_juntos = form.tempo_juntos.data
        current_user.aniversario = form.aniversario.data
        current_user.about_me = form.about_me.data  # corrigido aqui

        if form.profile_img.data:
            filename = secure_filename(form.profile_img.data.filename)
            path = os.path.join(app.root_path, 'static', 'uploads')
            os.makedirs(path, exist_ok=True)
            form.profile_img.data.save(os.path.join(path, filename))
            current_user.profile_img = filename

        db.session.commit()
        flash('Alterações salvas com sucesso!')
        return redirect(url_for('user', username=current_user.username))

    elif request.method == 'GET':
        form.nome.data = current_user.name
        form.cidade_estado.data = current_user.cidade_estado
        form.tempo_juntos.data = current_user.tempo_juntos
        form.aniversario.data = current_user.aniversario
        form.about_me.data = current_user.about_me  # corrigido aqui

    return render_template('editar_perfil.html', form=form, user=current_user)



@app.route('/marketplace')
def marketplace():
    return render_template('marketplace.html')