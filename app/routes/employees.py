from flask_appbuilder import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from ..interfaces import BaseModelRestApi
from ..models.employees import Employee, Department, Function


class EmployeeApi(BaseModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True

    datamodel = SQLAInterface(Employee)
    resource_name = "employees"

    list_columns = ['full_name', 'department', 'employee_number']


class FunctionApi(BaseModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True

    datamodel = SQLAInterface(Function)
    resource_name = "functions"

    related_apis = [EmployeeApi]


class DepartmentApi(BaseModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True
    datamodel = SQLAInterface(Department)
    resource_name = "departments"

    related_apis = [EmployeeApi]
