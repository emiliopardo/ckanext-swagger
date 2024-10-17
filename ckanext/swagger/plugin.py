import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint, jsonify, current_app

swagger_blueprint = Blueprint('swagger', __name__)

@swagger_blueprint.route('/swagger.json', methods=['GET'])
def swagger_json():
    api_base_url = toolkit.config.get('ckan.site_url') + '/api/3'
    
    # Obtener las rutas activas de CKAN desde la aplicación Flask
    paths = {}
    for rule in current_app.url_map.iter_rules():
        if rule.rule.startswith('/api'):  # Solo incluimos las rutas que empiezan por '/api'
            # Construimos la entrada para Swagger en base a la ruta
            path_data = {
                "get": {
                    "description": f"Endpoint for {rule.endpoint}",
                    "responses": {
                        "200": {
                            "description": "OK"
                        }
                    }
                }
            }
            paths[rule.rule] = path_data

    # Generar el archivo Swagger JSON de forma dinámica
    swagger_json_data = {
        "openapi": "3.0.0",
        "info": {
            "title": "CKAN API",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": api_base_url
            }
        ],
        "paths": paths
    }

    return jsonify(swagger_json_data)

# El plugin principal
class SwaggerPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    def get_blueprint(self):
        return swagger_blueprint

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'swagger')
