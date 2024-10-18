from ckan.plugins import SingletonPlugin, implements, IBlueprint
from ckanext.swagger.controllers.swagger import swagger_static_blueprint, swagger_dynamic_blueprint

class CKANSwaggerPlugin(SingletonPlugin):
    implements(IBlueprint)

    def get_blueprint(self):
        """
        Registro de los blueprints para servir el swagger.json estático y dinámico.
        """
        # Registrar ambos blueprints
        return [swagger_static_blueprint, swagger_dynamic_blueprint]
