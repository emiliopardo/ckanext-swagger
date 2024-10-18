from flask import jsonify, request  # Importar el objeto request para acceder a la solicitud actual
from ckan.plugins import toolkit

class SwaggerController:

    # Generar el archivo swagger.json dinámicamente
    @staticmethod
    def swagger_json():
        # Intentar obtener la lista de acciones de CKAN
        try:
            # Verificar si 'action_summary' existe en la respuesta de status_show
            status = toolkit.get_action('status_show')({})
            actions = status.get('action_summary', None)
            
            # Si no existe 'action_summary', intentamos usar otra estrategia
            if actions is None:
                # Obtener todas las acciones usando toolkit directamente
                actions = toolkit.get_actions()
        except KeyError:
            return jsonify({'error': 'No se pudo obtener la lista de acciones de CKAN'})

        # Obtener el host y esquema (http/https) de la solicitud actual
        host_url = request.host  # Esto obtiene "localhost:5000" o el host que se esté utilizando
        scheme = request.scheme  # Esto obtiene "http" o "https" según la solicitud

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
            "host": host_url,  # Usar el host dinámico
            "basePath": "/",
            "schemes": [scheme],  # Usar http o https dinámicamente según la solicitud
            "paths": paths
        }

        # Retornar la especificación Swagger como JSON
        return jsonify(swagger_spec)
