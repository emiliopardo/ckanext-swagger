from flask import Blueprint, jsonify
from flask_restx import Api
from ckan.plugins import toolkit
import os

# Crear un blueprint para manejar las rutas de Swagger
swagger_blueprint = Blueprint('swagger', __name__)

# Instanciar Flask-Restx para manejar la documentación Swagger
api = Api(swagger_blueprint, version='1.0', title='CKAN API Documentation',
          description='Documentación automática de la API de CKAN y Datastore')

# Controlador que servirá las páginas de Swagger UI y swagger.json
class SwaggerController:
    # Obtener todas las acciones de CKAN
    @staticmethod
    def get_ckan_actions():
        """Obtiene todas las acciones registradas en CKAN."""
        status = toolkit.get_action('status_show')({})
        return status['action_summary']

    # Generar el archivo swagger.json dinámicamente
    @staticmethod
    def swagger_json():
        # Obtener las acciones de CKAN
        actions = SwaggerController.get_ckan_actions()

        # Crear la estructura Swagger
        paths = {}
        for action_name in actions.keys():
            paths[f"/api/3/action/{action_name}"] = {
                "post": {
                    "summary": f"Invoca la acción {action_name}",
                    "description": f"Invoca la acción {action_name} en CKAN.",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "description": f"Parámetros para la acción {action_name}",
                            "schema": {
                                "type": "object",
                                "properties": {}
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Respuesta exitosa"
                        },
                        "400": {
                            "description": "Error en la solicitud"
                        }
                    }
                }
            }

        # Construir la especificación Swagger completa
        swagger_spec = {
            "swagger": "2.0",
            "info": {
                "version": "1.0",
                "title": "CKAN API",
                "description": "Documentación dinámica de la API de CKAN."
            },
            "host": "localhost:5000",  # Cambiar al host de tu instancia de CKAN
            "basePath": "/",
            "schemes": ["http"],
            "paths": paths
        }

        # Retornar la especificación Swagger como JSON
        return jsonify(swagger_spec)

    # Servir el Swagger UI
    @staticmethod
    def swagger_ui():
        # Ruta hacia el archivo index.html de Swagger UI
        swagger_ui_path = os.path.join(os.path.dirname(__file__), '../public/swagger/index.html')
        with open(swagger_ui_path, 'r') as swagger_ui_file:
            swagger_ui_content = swagger_ui_file.read()
        return swagger_ui_content
