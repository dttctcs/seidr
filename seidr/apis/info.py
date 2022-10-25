from flask_login import login_required
from flask_appbuilder.api import BaseApi, expose

from seidr.interfaces import SeidrApi


class InfoApi(BaseApi):
    resource_name = "info"
    openapi_spec_tag = "Info"

    security_level_apis = ['PermissionsApi', 'RolesApi', 'UsersApi', 'ViewsMenusApi', 'PermissionViewApi']
    excluded_apis = ['OpenApi', 'MenuApi', 'SecurityApi', 'InfoApi', 'AuthApi']

    @expose("/", methods=["GET"])
    @login_required
    def get_info(self):
        """An endpoint for retreiving the menu.
        ---
        get:
          description: >-
            Get the api structure.
            Returns a forest like structure with details about the ip
          responses:
            200:
              description: Get Info
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      apis:
                        description: Api items in a list
                        type: array
                        items:
                          type: object
                          properties:
                            name:
                              description: >-
                                The internal api name, maps to permission_name
                              type: string
                            type:
                              description: Api type. One of [security, default]
                              type: string
                            level:
                              description: Api permission level
                              type: string
            401:
              $ref: '#/components/responses/401'
        """

        seidr_apis = []
        for base_api in self.appbuilder.baseviews:
            if isinstance(base_api, BaseApi) and base_api.class_permission_name not in self.excluded_apis:
                name = base_api.list_title if isinstance(base_api,
                                                         SeidrApi) else base_api.resource_name.capitalize()
                icon = base_api.icon if hasattr(base_api, 'icon') else ''
                path = base_api.resource_name
                api_type = 'default' if not isinstance(base_api, SeidrApi) else 'table'
                level = 'default' if base_api.class_permission_name not in self.security_level_apis else 'security'
                permission_name = base_api.class_permission_name

                seidr_apis.append(
                    {'name': name, 'icon': icon, 'permission_name': permission_name, 'path': path,
                     'type': api_type, 'level': level})

        return self.response(200, **{"apis": seidr_apis})
