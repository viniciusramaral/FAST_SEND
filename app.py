from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from ma import ma
from db import db

from resources.book import Book, BookList, book_ns
from resources.instancia import Instancia, InstanciaList, instancia_ns
from resources.lead import Lead, LeadList, lead_ns
from resources.whats_message import Whats_message, WhatsMessageList, WhatsMessageSend, whats_message_ns


from marshmallow import ValidationError

from server.instance import server

api = server.api
app = server.app


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


api.add_resource(Book, '/books/<int:id>')
api.add_resource(BookList, '/books')


api.add_resource(Instancia, '/instancias/<int:id>')
api.add_resource(InstanciaList, '/instancias')

api.add_resource(Lead, '/leads/<int:id>')
api.add_resource(LeadList, '/leads')

api.add_resource(Whats_message, '/whats_messages/<int:id>')
api.add_resource(WhatsMessageList, '/whats_messages')
api.add_resource(WhatsMessageSend, '/whats_messages/disparo/<int:token>')



if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    server.run()
