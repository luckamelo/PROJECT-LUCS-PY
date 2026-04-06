from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50))

class Instituicao(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200))
    endereco = db.Column(db.String(200))
    responsavel = db.Column(db.String(100))

class Log(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100))
    acao = db.Column(db.String(200))
    data = db.Column(db.DateTime, default=datetime.datetime.utcnow)
