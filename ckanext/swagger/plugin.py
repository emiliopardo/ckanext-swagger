import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import jsonify


class SwaggerPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def get_blueprint(self):
        return [
            {
                "url": "/swagger",
                "controller": SwaggerController,
                "action": "swagger_ui",
                "methods": ["GET"]
            }
        ]
    
    def update_config_schema(self, schema):
        return schema

    def modify_navigation(self, nav_menu):
        nav_menu.add(_('API Docs'), h.url_for('swagger_ui'))
        return nav_menu

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'swagger')

class SwaggerController(plugins.toolkit.BaseController):
    def swagger_ui(self):
        return tk.render('swagger_ui.html')

    def swagger_json(self):
        api_base_url = tk.config.get('ckan.site_url') + '/api/3'
        swagger_json = {
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
                },
                # Add other endpoints dynamically
            }
        }
        return jsonify(swagger_json)