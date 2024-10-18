from ckan.plugins import toolkit, SingletonPlugin, implements
from flask import Blueprint
import ckan.plugins as p

class CKANSwaggerPlugin(SingletonPlugin):
    implements(p.IBlueprint)

    def get_blueprint(self):
        # Crear un blueprint de Flask para registrar las rutas
        swagger_blueprint = Blueprint('swagger', __name__)

        # Registrar la ruta para Swagger UI
        @swagger_blueprint.route('/api/swagger')
        def swagger_ui():
            from ckanext.swagger.controllers.swagger import SwaggerController
            return SwaggerController.swagger_ui()

        # Registrar la ruta para el archivo swagger.json
        @swagger_blueprint.route('/api/swagger.json')
        def swagger_json():
            from ckanext.swagger.controllers.swagger import SwaggerController
            return SwaggerController.swagger_json()

        return swagger_blueprint
