import os
from flask import Blueprint, send_from_directory
from ckan.plugins import SingletonPlugin, implements
from ckan.plugins.interfaces import IBlueprint, IConfigurer
from ckan.plugins.toolkit import config, add_template_directory, add_public_directory, add_resource

class SwaggerPlugin(SingletonPlugin):
    implements(IConfigurer, inherit=True)
    implements(IBlueprint, inherit=True)

    def update_config(self, config):
        """
        Este método se llama durante la fase de configuración de CKAN.
        Se utiliza para agregar directorios de plantillas, estáticos y configuraciones.
        """
        # Agregar directorio de plantillas
        add_template_directory(config, 'templates')

        # Agregar el directorio público (archivos estáticos como CSS y JS)
        add_public_directory(config, 'public')

        # Agregar recursos estáticos adicionales si es necesario
        add_resource('public', 'swagger')

    def get_blueprint(self):
        """
        Método para definir las rutas de tu plugin usando Flask Blueprint.
        """
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
            # Directorio donde se encuentra el index.html de Swagger UI
            static_folder = os.path.join(os.path.dirname(__file__), 'public', 'swagger-ui')
            return send_from_directory(static_folder, 'index.html')

        return swagger_blueprint
