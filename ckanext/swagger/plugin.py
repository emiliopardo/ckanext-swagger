from ckan.plugins import SingletonPlugin, implements
from ckan.plugins import IRoutes

class CKANSwaggerPlugin(SingletonPlugin):
    implements(IRoutes)

    def before_map(self, map):
        # Registrar las rutas para Swagger UI y el swagger.json dinámico
        map.connect('swagger_ui', 'api/swagger', controller='ckanext.swagger.controllers.swagger:SwaggerController', action='swagger_ui')
        map.connect('swagger_json', '/api/swagger.json', controller='ckanext.swagger.controllers.swagger:SwaggerController', action='swagger_json')
        return map
