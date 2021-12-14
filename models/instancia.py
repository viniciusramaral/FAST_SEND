from db import db
from typing import List
#from lead import LeadModel
from models.lead import LeadModel
from models.whats_message import  WhatsMessageModel

class InstanciaModel(db.Model):
    __tablename__ = "instancias"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False, unique=True)
    token = db.Column(db.String(80), nullable=False)
    leads = db.relationship('LeadModel')
    messages = db.relationship('WhatsMessageModel')



    def __init__(self, nome, token):
        self.nome = nome
        self.token = token

    def __repr__(self):
        return f'InstanciaModel(nome={self.nome}, token={self.token})'

    def json(self):
        return {'nome': self.nome, 'token': self.token}

    @classmethod
    def find_by_nome(cls, nome) -> "InstanciaModel":
        return cls.query.filter_by(nome=nome).first()

    @classmethod
    def find_by_id(cls, _id) -> "InstanciaModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["InstanciaModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
