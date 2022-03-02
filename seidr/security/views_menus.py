from flask_appbuilder.security.sqla.models import ViewMenu
from flask_appbuilder.models.sqla.interface import SQLAInterface

from seidr.interfaces import BaseModelRestApi


class ViewsMenusApi(BaseModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True
    datamodel = SQLAInterface(ViewMenu)

    # this also effects schema of related models
    page_size = 200
    max_page_size = 200

    resource_name = "viewsmenus"
    base_permissions = ['can_get', 'can_info']
