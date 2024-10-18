from flask import Blueprint, jsonify, request, send_file
from ckan.plugins import toolkit
import ckan.logic.action as action
import os

# Blueprint para swagger estático
swagger_static_blueprint = Blueprint('swagger_static', __name__)

# Blueprint para swagger dinámico
swagger_dynamic_blueprint = Blueprint('swagger_dynamic', __name__)

class SwaggerController:
    # Ruta para servir el archivo swagger.json estático
    @swagger_static_blueprint.route('/api/static/swagger.json')
    def swagger_static():
        # Ruta del archivo swagger.json estático
        static_file_path = os.path.join(os.path.dirname(__file__), '../public/swagger/swagger.json')
        return send_file(static_file_path)

    # Generar el archivo swagger.json dinámico
    @swagger_dynamic_blueprint.route('/api/dynamic/swagger.json')
    def swagger_dynamic():
        try:
            # Obtener todas las acciones de CKAN desde ckan.logic.action.get
            actions = {}
            for action_name in dir(action.get):
                if not action_name.startswith("_"):  # Ignorar métodos privados
                    try:
                        # Obtener la función de la acción
                        action_function = toolkit.get_action(action_name)
                        actions[action_name] = action_function
                    except toolkit.ObjectNotFound:
                        continue  # Saltar si la acción no está disponible

            # Obtener el host y esquema (http/https) de la solicitud actual
            host_url = request.host
            scheme = request.scheme

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
                "host": host_url,
                "basePath": "/",
                "schemes": [scheme],
                "paths": paths
            }

            # Retornar la especificación Swagger como JSON
            return jsonify(swagger_spec)

        except Exception as e:
            return jsonify({"error": str(e)})
