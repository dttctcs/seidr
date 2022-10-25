from flask_appbuilder.security.sqla.models import PermissionView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from seidr.interfaces import SeidrApi


class PermissionViewApi(SeidrApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True
    datamodel = SQLAInterface(PermissionView)

    # this also effects schema of related models
    page_size = 200
    max_page_size = 200

    resource_name = "permissionview"
    base_permissions = ['can_get', 'can_info']
