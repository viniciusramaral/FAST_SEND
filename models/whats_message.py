from db import db
from typing import List


class WhatsMessageModel(db.Model):
    __tablename__ = "whatsMessages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mymessage = db.Column(db.Text(), nullable=True, unique=False)
    urllink = db.Column(db.Text(), nullable=True, unique=False)
    #instancia_id = db.Column(db.Integer, nullable=False)
    instancia_id = db.Column(db.Integer, db.ForeignKey('instancias.id'), nullable=False)


    def __init__(self, mymessage, urllink, instancia_id):
        self.mymessage = mymessage
        self.urllink = urllink
        self.instancia_id = instancia_id

    def __repr__(self):
        return f'WhatsMessageModel(mymessage={self.mymessage}, urllink={self.urllink}, instancia_id={self.instancia_id})'

    def json(self):
        return {'mymessage': self.mymessage, 'urllink': self.urllink, 'instancia_id': self.instancia_id}

    @classmethod
    def find_by_mymessage(cls, mymessage) -> "WhatsMessageModel":
        return cls.query.filter_by(mymessage=mymessage).first()

    @classmethod
    def find_by_id(cls, _id) -> "WhatsMessageModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["WhatsMessageModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
