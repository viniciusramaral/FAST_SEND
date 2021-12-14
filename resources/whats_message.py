from flask import request
from flask_restplus import Resource, fields

from models.whats_message import WhatsMessageModel
from schemas.whats_message import WhatsMessageSchema

from server.instance import server

from tasks.envio_em_lote import EnvioEmLote

whats_message_ns = server.whats_message_ns

ITEM_NOT_FOUND = "Whats_message not found."


whats_message_schema = WhatsMessageSchema()
whats_message_list_schema = WhatsMessageSchema(many=True)

# Model required by flask_restplus for expect
item = whats_message_ns.model('Whats_message', {
    'mymessage': fields.String('Whats_message'),
    'urllink': fields.String('Link público'),
    'instancia_id': fields.Integer('Id da Instância de envio'),
})


class Whats_message(Resource):

    def get(self, id):
        whats_message_data = WhatsMessageModel.find_by_id(id)
        if whats_message_data:
            return whats_message_schema.dump(whats_message_data)
        return {'message': ITEM_NOT_FOUND}, 404

    def delete(self, id):
        whats_message_data = WhatsMessageModel.find_by_id(id)
        if whats_message_data:
            whats_message_data.delete_from_db()
            return '', 204
        return {'message': ITEM_NOT_FOUND}, 404

    @whats_message_ns.expect(item)
    def put(self, id):
        whats_message_data = WhatsMessageModel.find_by_id(id)
        whats_message_json = request.get_json()

        if whats_message_data:
            whats_message_data.urllink = whats_message_json['urllink']
            whats_message_data.mymessage = whats_message_json['mymessage']
            whats_message_data.urllink = whats_message_json['urllink']
            whats_message_data.instancia_id = whats_message_json['instancia_id']
        else:
            whats_message_data = whats_message_schema.load(whats_message_json)

        whats_message_data.save_to_db()
        return whats_message_schema.dump(whats_message_data), 200


class WhatsMessageList(Resource):
    @whats_message_ns.doc('Get all the Items')
    def get(self):
        return whats_message_list_schema.dump(WhatsMessageModel.find_all()), 200

    @whats_message_ns.expect(item)
    @whats_message_ns.doc('Create an Item')
    def post(self):
        whats_message_json = request.get_json()
        whats_message_data = whats_message_schema.load(whats_message_json)

        whats_message_data.save_to_db()

        return whats_message_schema.dump(whats_message_data), 201


class WhatsMessageSend(Resource):
    @whats_message_ns.doc('Get all the Items')
    def get(self, token):
        print (token)

        sends = whats_message_list_schema.dump(WhatsMessageModel.find_all())

        EnvioEmLote(sends)


        return whats_message_list_schema.dump(WhatsMessageModel.find_all()), 200
