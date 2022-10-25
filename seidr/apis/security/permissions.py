from flask_appbuilder.security.sqla.models import Permission
from flask_appbuilder.models.sqla.interface import SQLAInterface

from seidr.interfaces import SeidrApi


class PermissionsApi(SeidrApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True
    datamodel = SQLAInterface(Permission)

    # this also effects schema of related models
    page_size = 200
    max_page_size = 200

    resource_name = "permissions"
    base_permissions = ['can_get', 'can_info']
