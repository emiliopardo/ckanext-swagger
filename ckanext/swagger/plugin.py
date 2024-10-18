from ckan.plugins import SingletonPlugin, implements, IBlueprint, IRoutes
from ckanext.swagger.controllers.swagger import swagger_static_blueprint, swagger_dynamic_blueprint
from flask import render_template

class CKANSwaggerPlugin(SingletonPlugin):
    implements(IBlueprint, IRoutes)

    def get_blueprint(self):
        """
        Registro de los blueprints para servir el swagger.json estático y dinámico.
        """
        # Registrar ambos blueprints
        return [swagger_static_blueprint, swagger_dynamic_blueprint]

    def before_map(self, map):
        """
        Mapeo de la ruta para servir la interfaz Swagger UI.
        """
        map.connect(
            'swagger_ui',  # Nombre de la ruta
            '/swagger',    # URL que servirá la interfaz Swagger
            controller='ckanext.swagger.controllers.swagger:SwaggerUIController',
            action='show'
        )
        return map
