from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from typing import Optional

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # Campos antes em Perfil:
    profile_img: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    cidade_estado: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
    tempo_juntos: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
    aniversario: so.Mapped[Optional[datetime]] = so.mapped_column(sa.Date())
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    posts: so.Mapped[list['Post']] = so.relationship(back_populates='author', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(280))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return f'<Post {self.body[:30]}...>'
    
class Memoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Date, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(100))  # Caminho para imagem
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Memoria {self.titulo}>'
