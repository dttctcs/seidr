from flask_appbuilder.api import BaseApi, expose

from flask import current_app
from flask_login import login_required


class MenuApi(BaseApi):
    resource_name = "menu"
    openapi_spec_tag = "Menu"

    @expose("/", methods=["GET"])
    @login_required
    def get_menu_data(self):
        """An endpoint for retreiving the menu.
        ---
        get:
          description: >-
            Get the menu data structure.
            Returns a forest like structure with the menu the user has access to
          responses:
            200:
              description: Get menu data
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      result:
                        description: Menu items in a forest like data structure
                        type: array
                        items:
                          type: object
                          properties:
                            name:
                              description: >-
                                The internal menu item name, maps to permission_name
                              type: string
                            label:
                              description: Pretty name for the menu item
                              type: string
                            icon:
                              description: Icon name to show for this menu item
                              type: string
                            url:
                              description: The URL for the menu item
                              type: string
                            childs:
                              type: array
                              items:
                                type: object
            401:
              $ref: '#/components/responses/401'
        """
        allowed_menus = current_app.appbuilder.sm.get_user_menu_access(
            self.get_flat_name_list()
        )
        return self.response(200, result=current_app.appbuilder.menu.get_data())
