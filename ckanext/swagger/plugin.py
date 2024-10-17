import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint, jsonify, current_app, render_template

swagger_blueprint = Blueprint('swagger', __name__)

# Ruta para servir el JSON de Swagger dinámicamente
@swagger_blueprint.route('/swagger.json', methods=['GET'])
def swagger_json():
    api_base_url = toolkit.config.get('ckan.site_url') + '/api/3'
    
    # Obtener las rutas activas de CKAN desde la aplicación Flask
    paths = {}
    for rule in current_app.url_map.iter_rules():
        if rule.rule.startswith('/api/3/action'):  # Solo incluimos las rutas que empiezan por '/api/3/action'
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

# Ruta para servir la interfaz Swagger UI a través del template
@swagger_blueprint.route('/swagger', methods=['GET'])
def swagger_ui():
    # Renderizar el template que mostrará la interfaz de Swagger UI
    return render_template('swagger_ui.html')

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
