from flask_appbuilder.models.sqla.interface import SQLAInterface

from ..interfaces import BaseModelRestApi
from ..models.employees import Employee, Department, Function


class FunctionApi(BaseModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True

    datamodel = SQLAInterface(Function)
    resource_name = "functions"


class EmployeeApi(BaseModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True

    datamodel = SQLAInterface(Employee)
    resource_name = "employees"

    list_columns = ['full_name', 'address', 'fiscal_number', 'department', 'employee_number']
    related_apis = [FunctionApi]


class DepartmentApi(BaseModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True

    datamodel = SQLAInterface(Department)
    resource_name = "departments"

    related_apis = [EmployeeApi]
