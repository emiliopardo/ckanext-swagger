import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint, jsonify, render_template

# Definimos el blueprint de Flask
swagger_blueprint = Blueprint('swagger', __name__)

# Ruta para la UI de Swagger
@swagger_blueprint.route('/swagger', methods=['GET'])
def swagger_ui():
    return toolkit.render('swagger_ui.html')

# Ruta para el JSON de Swagger
@swagger_blueprint.route('/swagger.json', methods=['GET'])
def swagger_json():
    api_base_url = toolkit.config.get('ckan.site_url') + '/api/3'
    swagger_json_data = {
        "openapi": "3.0.0",
        "info": {
            "title": "CKAN API",
            "version": "1.0.0"
        },
        "paths": {
            "/": {
                "get": {
                    "description": "Retrieve API information",
                    "responses": {
                        "200": {
                            "description": "OK"
                        }
                    }
                }
            }
        }
    }
    return jsonify(swagger_json_data)

# El plugin principal
class SwaggerPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    # Método para devolver el blueprint (Flask) que maneja las rutas
    def get_blueprint(self):
        return swagger_blueprint

    # Método para configurar los directorios de plantillas, recursos públicos, etc.
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'swagger')

