from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.models.sqla.interface import SQLAInterface

from seidr.interfaces import BaseModelRestApi


class UsersApi(BaseModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True
    datamodel = SQLAInterface(User)

    resource_name = "users"
    list_columns = ["first_name", "last_name", "username", "email", "active", "login_count", "roles"]
    label_columns = {"username": "Benutzername", "first_name": 'Vorname', "last_name": "Nachname", "email": "Email",
                     "active": 'Aktiv', "login_count": "Anzahl Logins", "roles": "Rollen "}
    show_exclude_columns = ["password", "changed"]
    edit_columns = ["first_name", "last_name", "username", "email", "active", "roles"]
    add_columns = ["first_name", "last_name", "username", "active", "email", "roles", "password"]