from flask import url_for

from flask_appbuilder import BaseView, expose
from flask_appbuilder.api.manager import OpenApi

class OpenAPIView(BaseView):
    route_base = "/openapi"
    default_view = "show"

    @expose("/<version>")
    def show(self, version):
        return self.render_template(
            self.appbuilder.app.config.get(
                "FAB_API_SWAGGER_TEMPLATE", "appbuilder/swagger/swagger.html"
            ),
            openapi_uri=url_for(OpenApi.__name__ + '.' + OpenApi.get.__name__, version=version),
        )
