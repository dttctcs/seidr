import datetime

from flask import g
from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.models.sqla.interface import SQLAInterface
from werkzeug.security import generate_password_hash

from seidr.interfaces import SeidrApi


class UsersApi(SeidrApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True
    datamodel = SQLAInterface(User)

    resource_name = "users"
    list_columns = ["first_name", "last_name", "username", "email", "active", "last_login", "login_count", "roles"]
    label_columns = {"username": "Benutzername", "first_name": 'Vorname', "last_name": "Nachname", "email": "Email",
                     "active": 'Aktiv', "login_count": "Anzahl Logins", "roles": "Rollen "}
    show_exclude_columns = ["password", "changed"]
    search_columns = ["username", "first_name", "last_name", "active", "email", "created_by", "changed_by", "roles"]
    edit_columns = ["first_name", "last_name", "username", "email", "active", "roles"]
    add_columns = ["first_name", "last_name", "username", "active", "email", "roles", "password"]

    def pre_update(self, item):
        item.changed_on = datetime.datetime.now()
        item.changed_by_fk = g.user.id

    def pre_add(self, item):
        item.password = generate_password_hash(item.password)
