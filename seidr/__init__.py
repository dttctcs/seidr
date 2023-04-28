from seidr.apis import AuthApi, InfoApi, PermissionViewApi, PermissionsApi, RolesApi, UsersApi, ViewsMenusApi
from flask import Flask, render_template_string, send_file
from flask_appbuilder.api.manager import OpenApi
from .views import OpenAPIView, SeidrIndexView
import io
class Seidr(object):

    def __init__(self, appbuilder):
        self.appbuilder = appbuilder
        self.appbuilder.seidr = self
        self.appbuilder.app.config.setdefault("SEIDR_AUTH", True)
        self.appbuilder.app.config.setdefault("SEIDR_INFO", True)
        self.appbuilder.app.config.setdefault("SEIDR_SECU", True)
        self.appbuilder.app.config.setdefault("SEIDR_OPENAPI_UI", True)
        self.appbuilder.app.config.setdefault("SEIDR_REACT_CONFIG", {})
        
        if self.appbuilder.app.config.get("SEIDR_AUTH"):
            self.appbuilder.add_api(AuthApi)
        if self.appbuilder.app.config.get("SEIDR_INFO"):
            self.appbuilder.add_api(InfoApi)
        if self.appbuilder.app.config.get("SEIDR_SECU"):
            self.appbuilder.add_api(AuthApi)
            self.appbuilder.add_api(PermissionViewApi)
            self.appbuilder.add_api(PermissionsApi)
            self.appbuilder.add_api(RolesApi)
            self.appbuilder.add_api(UsersApi)
            self.appbuilder.add_api(ViewsMenusApi)

        if self.appbuilder.app.config.get("SEIDR_OPENAPI_UI"):
            self.appbuilder.add_api(OpenApi)
            self.appbuilder.add_view_no_menu(OpenAPIView)

        @self.appbuilder.app.route('/server-config.js', methods=['GET'])
        def js_manifest():
            content = render_template_string('window.seid_react_config = {{ react_vars |tojson }}',
                                    react_vars=self.appbuilder.app.config["SEIDR_REACT_CONFIG"]).encode('utf-8')
            scriptfile = io.BytesIO(content)
            return send_file(scriptfile, mimetype='application/javascript', download_name="server-config.js")            
