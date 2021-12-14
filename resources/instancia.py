from flask import request
from flask_restplus import Resource, fields

from models.instancia import InstanciaModel
from schemas.instancia import Instanciaschema

from server.instance import server

instancia_ns = server.instancia_ns

ITEM_NOT_FOUND = "Instancia not found."


instancia_schema = Instanciaschema()
instancia_list_schema = Instanciaschema(many=True)

# Model required by flask_restplus for expect
item = instancia_ns.model('Instancia', {
    'nome': fields.String('Instancia nome'),
    'token': fields.String('Token da Instância'),
})


class Instancia(Resource):

    def get(self, id):
        instancia_data = InstanciaModel.find_by_id(id)
        if instancia_data:
            return instancia_schema.dump(instancia_data)
        return {'message': ITEM_NOT_FOUND}, 404

    def delete(self, id):
        instancia_data = InstanciaModel.find_by_id(id)
        if instancia_data:
            instancia_data.delete_from_db()
            return '', 204
        return {'message': ITEM_NOT_FOUND}, 404

    @instancia_ns.expect(item)
    def put(self, id):
        instancia_data = InstanciaModel.find_by_id(id)
        instancia_json = request.get_json()

        if instancia_data:
            instancia_data.token = instancia_json['token']
            instancia_data.nome = instancia_json['nome']
        else:
            instancia_data = instancia_schema.load(instancia_json)

        instancia_data.save_to_db()
        return instancia_schema.dump(instancia_data), 200


class InstanciaList(Resource):
    @instancia_ns.doc('Get all the Items')
    def get(self):
        return instancia_list_schema.dump(InstanciaModel.find_all()), 200

    @instancia_ns.expect(item)
    @instancia_ns.doc('Create an Item')
    def post(self):
        instancia_json = request.get_json()
        instancia_data = instancia_schema.load(instancia_json)

        instancia_data.save_to_db()

        return instancia_schema.dump(instancia_data), 201
