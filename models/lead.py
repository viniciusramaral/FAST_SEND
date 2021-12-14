
from db import db
from typing import List

class LeadModel(db.Model):
    __tablename__ = "leads"
    __table_args__ = (
        # this can be db.PrimaryKeyConstraint if you want it to be a primary key
        db.UniqueConstraint('phone', 'instancia_id'),
      )
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False, unique=False)
    phone = db.Column(db.Integer, nullable=False)
    blocked = db.Column(db.Boolean, nullable=False)
    #instancia_id = db.Column(db.Integer, nullable=False)
    instancia_id = db.Column(db.Integer, db.ForeignKey('instancias.id'), nullable=False)



    def __init__(self, nome, phone, instancia_id, blocked):
        self.nome = nome
        self.phone = phone
        self.instancia_id = instancia_id
        self.blocked = blocked

    def __repr__(self):
        return f'LeadModel(nome={self.nome}, phone={self.phone}, instancia_id={self.instancia_id}, blocked={self.blocked}'

    def json(self):
        return {'nome': self.nome, 'phone': self.phone, 'instancia_id': self.instancia_id, 'blocked': self.blocked}

    @classmethod
    def find_by_nome(cls, nome) -> "LeadModel":
        return cls.query.filter_by(nome=nome).first()

    @classmethod
    def find_by_id(cls, _id) -> "LeadModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["LeadModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
