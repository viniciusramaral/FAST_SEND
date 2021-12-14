from ma import ma
from models.instancia import InstanciaModel


class Instanciaschema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InstanciaModel
        load_instance = True
