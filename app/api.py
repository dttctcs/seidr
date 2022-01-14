from app import appbuilder
from app.routes.employees import EmployeeApi, FunctionApi, DepartmentApi

from app.routes.security.auth import AuthApi
from app.routes.security.user import UserApi
from app.routes.security.users import UsersApi
from app.routes.security.roles import RolesApi
from app.routes.security.permissions import PermissionsApi
from app.routes.security.views_menus import ViewsMenusApi
from app.routes.security.permission_view import PermissionViewApi

appbuilder.add_api(AuthApi)
appbuilder.add_api(UserApi)
appbuilder.add_api(UsersApi)
appbuilder.add_api(RolesApi)
appbuilder.add_api(PermissionsApi)
appbuilder.add_api(ViewsMenusApi)
appbuilder.add_api(PermissionViewApi)

appbuilder.add_api(EmployeeApi)
appbuilder.add_api(FunctionApi)
appbuilder.add_api(DepartmentApi)


