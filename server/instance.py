from flask import Flask, Blueprint
from flask_restplus import Api
from ma import ma
from db import db

from marshmallow import ValidationError


class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.bluePrint = Blueprint('api', __name__, url_prefix='/api')
        self.api = Api(self.bluePrint, doc='/doc', title='Sample Flask-RestPlus Application')
        self.app.register_blueprint(self.bluePrint)

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['PROPAGATE_EXCEPTIONS'] = True

        self.book_ns = self.book_ns()
        self.instancia_ns = self.instancia_ns()
        self.lead_ns = self.lead_ns()
        self.whats_message_ns = self.whats_message_ns()


        super().__init__()

    def book_ns(self, ):
        return self.api.namespace(name='Books', description='book related operations', path='/')

    def instancia_ns(self, ):
        return self.api.namespace(name='Instancias', description='instancia related operations', path='/')

    def lead_ns(self, ):
        return self.api.namespace(name='Leads', description='lead related operations', path='/')

    def whats_message_ns(self, ):
        return self.api.namespace(name='WhatsApp Message', description='lead related operations', path='/')



    def run(self, ):
        self.app.run(
            port=5000,
            debug=True,
            host='0.0.0.0'
        )


server = Server()
