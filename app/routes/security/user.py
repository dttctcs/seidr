from flask import g, request

from flask_appbuilder import expose
from flask_appbuilder.api import ModelRestApi, safe
from flask_appbuilder.security.decorators import has_access_api
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.sqla.models import User


class UserApi(ModelRestApi):
    datamodel = SQLAInterface(User)
    exclude_route_methods = ["put", "post", "delete", 'info', 'get', 'get_list']
    resource_name = "user"

    list_columns = ["first_name", "last_name", "username", "email", "active", "login_count", "roles"]
    show_columns = ["first_name", "last_name", "username", "email", "active", "login_count", "roles"]

    @has_access_api
    @expose('/userinfo')
    @safe
    def get_userinfo(self):
        """Userinfo endpoint for the API, returns user data
         ---
         get:
           description: >-
             Get user information
           responses:
             200:
               description: Received user information
             400:
               $ref: '#/components/responses/400'
             401:
               $ref: '#/components/responses/401'
             500:
               $ref: '#/components/responses/500'
         """

        # get public user data
        item = self.datamodel.get(g.user.id, select_columns=self.show_columns)
        response = self.show_model_schema.dump(item, many=False)
        return self.response(200, **response)

    @has_access_api
    @expose('/update', methods=["PUT"])
    @safe
    def update_userinfo(self):
        """Update user endpoint for the API, updates user data
             ---
             post:
               description: >-
                 Update user information
               requestBody:
                 required: true
                 content:
                   application/json:
                     schema:
                       type: object
                       properties:
                         firstname:
                           description: The username for authentication
                           example: john
                           type: string
                           required: true
                         lastname:
                           description: The password for authentication
                           example: doe
                           type: string
                           required: true
               responses:
                 200:
                   description: Update Successful
                 400:
                   $ref: '#/components/responses/400'
                 401:
                   $ref: '#/components/responses/401'
                 500:
                   $ref: '#/components/responses/500'
             """
        firstname = request.json.get('firstname', None)
        lastname = request.json.get('lastname', None)
        item = self.appbuilder.sm.get_user_by_id(g.user.id)

        # update user
        item.first_name = firstname
        item.last_name = lastname
        self.appbuilder.sm.update_user(item)

        # get public user data
        item = self.datamodel.get(g.user.id, select_columns=self.show_columns)
        response = self.show_model_schema.dump(item, many=False)
        return self.response(200, **response)

    @has_access_api
    @expose('/resetpassword', methods=["PUT"])
    @safe
    def reset_password(self):
        """Reset user password endpoint for the API, resets user password
             ---
             post:
               description: >-
                 Reset user password
               requestBody:
                 required: true
                 content:
                   application/json:
                     schema:
                       type: object
                       properties:
                         password:
                           description: The password to rest
                           example: complex-password
                           type: string
                           required: true
               responses:
                 200:
                   description: Update Successful
                 400:
                   $ref: '#/components/responses/400'
                 401:
                   $ref: '#/components/responses/401'
                 500:
                   $ref: '#/components/responses/500'
             """
        password = request.json.get('password', None)
        self.appbuilder.sm.reset_password(g.user.id, password)
        return self.response(200, message="Update successful")
