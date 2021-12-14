from ma import ma
from models.whats_message import WhatsMessageModel


class WhatsMessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WhatsMessageModel
        load_instance = True
        include_fk = True
