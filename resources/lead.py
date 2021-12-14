from flask import request
from flask_restplus import Resource, fields

from models.lead import LeadModel
from schemas.lead import LeadSchema

from server.instance import server

lead_ns = server.lead_ns

ITEM_NOT_FOUND = "Lead not found."


lead_schema = LeadSchema()
lead_list_schema = LeadSchema(many=True)

# Model required by flask_restplus for expect
item = lead_ns.model('Lead', {
    'nome': fields.String('Lead nome'),
    'phone': fields.Integer(0),
    'instancia_id': fields.Integer(0),
    'blocked': fields.Boolean(0),
})


class Lead(Resource):

    def get(self, id):
        lead_data = LeadModel.find_by_id(id)
        if lead_data:
            return lead_schema.dump(lead_data)
        return {'message': ITEM_NOT_FOUND}, 404

    def delete(self, id):
        lead_data = LeadModel.find_by_id(id)
        if lead_data:
            lead_data.delete_from_db()
            return '', 204
        return {'message': ITEM_NOT_FOUND}, 404

    @lead_ns.expect(item)
    def put(self, id):
        lead_data = LeadModel.find_by_id(id)
        lead_json = request.get_json()

        if lead_data:
            lead_data.phone = lead_json['phone']
            lead_data.nome = lead_json['nome']
            lead_data.instancia_id = lead_json['instancia_id']
            lead_data.blocked = lead_json['blocked']
        else:
            lead_data = lead_schema.load(lead_json)

        lead_data.save_to_db()
        return lead_schema.dump(lead_data), 200


class LeadList(Resource):
    @lead_ns.doc('Get all the Items')
    def get(self):
        return lead_list_schema.dump(LeadModel.find_all()), 200

    @lead_ns.expect(item)
    @lead_ns.doc('Create an Item')
    def post(self):
        lead_json = request.get_json()
        lead_data = lead_schema.load(lead_json)

        lead_data.save_to_db()

        return lead_schema.dump(lead_data), 201
