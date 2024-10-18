import os
from flask import Blueprint, send_from_directory
from ckan.plugins import SingletonPlugin, implements
from ckan.plugins.interfaces import IRoutes, IConfigurer
from ckan.plugins.toolkit import config

class SwaggerPlugin(SingletonPlugin):
    implements(IRoutes, inherit=True)
    implements(IConfigurer, inherit=True)

    def update_config(self, config):
        """
        Este método se llama durante la fase de configuración de CKAN.
        Se utiliza para agregar directorios de plantillas, estáticos y configuraciones.
        """
        # Agregar directorio de plantillas
        self.add_template_directory(config, 'templates')

        # Agregar el directorio público (archivos estáticos como CSS y JS)
        self.add_public_directory(config, 'public')

        # Agregar recursos (si tienes algo adicional)
        self.add_resource('public', 'swagger')

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
            return send_from_directory(os.path.join(os.path.dirname(__file__), 'public', 'swagger-ui'), 'index.html')

        return swagger_blueprint

    def before_map(self, map):
        """
        Este método es parte de la interfaz IRoutes. Aquí puedes agregar nuevas rutas.
        """
        # Aquí puedes mapear las rutas de Flask para asegurar que se registren
        map.connect('/swagger', controller='ckanext.swagger.plugin:SwaggerPlugin', action='swagger_ui')
        map.connect('/swagger.json', controller='ckanext.swagger.plugin:SwaggerPlugin', action='swagger_json')
        return map

    def after_map(self, map):
        """
        Si necesitas modificar el mapa de rutas después de que CKAN lo haya procesado.
        """
        return map
