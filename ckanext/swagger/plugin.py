import os
from flask import Blueprint, current_app, jsonify, send_from_directory
from ckan.plugins import SingletonPlugin, implements
from ckan.plugins.toolkit import config

class SwaggerPlugin(SingletonPlugin):
    # Implementación de la interfaz de plugins de CKAN
    implements(IBlueprint)

    def get_blueprint(self):
        # Definir un Blueprint para agregar las rutas
        swagger_blueprint = Blueprint('swagger', __name__)

        # Ruta para servir el archivo swagger.json
        @swagger_blueprint.route('/swagger.json')
        def swagger_json():
            # Ruta del archivo swagger.json estático
            swagger_file_path = os.path.join(os.path.dirname(__file__), 'swagger.json')
            return send_from_directory(os.path.dirname(swagger_file_path), 'swagger.json')

        # Ruta para servir Swagger UI
        @swagger_blueprint.route('/swagger')
        def swagger_ui():
            return send_from_directory(os.path.join(os.path.dirname(__file__), 'static', 'swagger-ui'), 'index.html')

        return swagger_blueprint

