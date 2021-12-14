from ma import ma
from models.lead import LeadModel


class LeadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LeadModel
        load_instance = True
        include_fk = True