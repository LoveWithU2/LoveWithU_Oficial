from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileAllowed

class RegistrationForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(min=2, max=64)])
    username = StringField('Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class CriarMemoriaForm(FlaskForm):
    titulo = StringField('Título da Memória', validators=[DataRequired()])
    data = DateField('Data', validators=[DataRequired()], format='%Y-%m-%d')
    categoria = SelectField('Categoria', choices=[
        ('viagem', 'Viagem'),
        ('aniversario', 'Aniversário'),
        ('mensagem', 'Mensagem'),
        ('passeio', 'Passeio'),
        ('outro', 'Outro')
    ])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    imagem = FileField('Imagem (opcional)', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Imagens apenas!')])

class EditarPerfilForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=64)])
    cidade_estado = StringField('Cidade/Estado')
    tempo_juntos = StringField('Tempo juntos')
    aniversario = DateField('Aniversário', format='%Y-%m-%d')
    about_me = TextAreaField('Sobre mim', validators=[Length(min=0, max=140)])
    profile_img = FileField('Imagem de perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Salvar')
