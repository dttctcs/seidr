import functools
import json
import urllib
from typing import Any, Callable, Optional, Dict
import jsonschema
import prison as prison
from flask_appbuilder.api import BaseApi, ModelRestApi, merge_response_func, expose, safe, rison, get_info_schema
from flask_appbuilder._compat import as_unicode

from flask_appbuilder.security.decorators import permission_name, protect
from flask import  Response, request
from flask_appbuilder.const import API_ADD_COLUMNS_RIS_KEY, API_ADD_TITLE_RIS_KEY, API_PERMISSIONS_RIS_KEY, \
    API_EDIT_COLUMNS_RIS_KEY, API_FILTERS_RIS_KEY, API_EDIT_TITLE_RIS_KEY, API_FILTERS_RES_KEY, \
    API_ORDER_COLUMNS_RIS_KEY, API_LABEL_COLUMNS_RIS_KEY, API_DESCRIPTION_COLUMNS_RIS_KEY, API_LIST_COLUMNS_RIS_KEY, \
    API_LIST_TITLE_RIS_KEY, API_URI_RIS_KEY
from flask_appbuilder.api.schemas import get_list_schema
from seidr.interfaces.convert import Model2SchemaConverter

from copy import deepcopy
def better_rison(
        schema: Optional[Dict[str, Any]] = None
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Use this decorator to parse URI *Rison* arguments to
    a python data structure, your method gets the data
    structure on kwargs['rison']. Response is HTTP 400
    if *Rison* is not correct::

        class ExampleApi(BaseApi):
                @expose('/risonjson')
                @rison()
                def rison_json(self, **kwargs):
                    return self.response(200, result=kwargs['rison'])

    You can additionally pass a JSON schema to
    validate Rison arguments::

        schema = {
            "type": "object",
            "properties": {
                "arg1": {
                    "type": "integer"
                }
            }
        }

        class ExampleApi(BaseApi):
                @expose('/risonjson')
                @rison(schema)
                def rison_json(self, **kwargs):
                    return self.response(200, result=kwargs['rison'])

    """

    def _rison(f: Callable[..., Any]) -> Callable[..., Any]:
        def wraps(self: "BaseApi", *args: Any, **kwargs: Any) -> Response:
            value = request.args.get(API_URI_RIS_KEY, None)
            kwargs["rison"] = dict()
            if value:
                try:
                    kwargs["rison"] = prison.loads(value)
                except prison.decoder.ParserException:
                    try:
                        kwargs["rison"] = json.loads(value)
                    except Exception:
                        return self.response_400(
                            message="Not a valid rison/json argument"
                        )
            if schema:
                try:
                    jsonschema.validate(instance=kwargs["rison"], schema=schema)
                except jsonschema.ValidationError as e:
                    return self.response_400(message=f"Not a valid rison schema {e}")
            return f(self, *args, **kwargs)

        return functools.update_wrapper(wraps, f)

    return _rison

class SeidrApi(ModelRestApi):
    allow_browser_login = True
    quick_filters = None
    filter_options = None
    search_model_schema = None
    search_query_rel_fields = None
    """
        List with quickfilters. Example:
        quick_filters = [
            {
                "name": "buStatic",
                "label": "Business Unit",
                "column": "name",
                "type": "multiselect",
                "options": [{"value": "Eurowings", "label": "Eurowings BU Label"}]
            },
        ]
    """
    icon = "Table"
    related_apis = []

    """
        List with ModelRestApi classes
        Will add related_apis information to the info endpoint

            class MyApi(SeidrApi):
                datamodel = SQLAModel(Group, db.session)
                related_apis = [MyOtherApi]

    """

    model2schemaconverter = Model2SchemaConverter

    def __init__(self):
        super().__init__()
        name = self.resource_name or self.__class__.__name__.lower()
        self.list_title = name.capitalize()
        self.quick_filters = self.quick_filters or []
        self.filter_options = self.filter_options or {}
        self.search_model_schema_name = f"{self.__class__.__name__}.search"

        self.search_query_rel_fields = self.search_query_rel_fields or dict()

        if self.search_model_schema is None:
            self.search_model_schema = self.model2schemaconverter.convert(
                self.search_columns,
                nested=False,
                parent_schema_name=self.search_model_schema_name,
            )

    def merge_relations_info(self, response, **kwargs):
        """
        Adds relationship information to the response
        :param response: The response object
        :param kwargs: api endpoint kwargs
        """
        relations = []
        for related_api in self.related_apis:
            foreign_key = related_api.datamodel.get_related_fk(self.datamodel.obj)
            relation_type = "rel_o_m" if related_api.datamodel.is_relation_many_to_one(foreign_key) else "rel_m_m"
            relation = {
                'name': related_api.list_title if related_api.list_title else self._prettify_name(
                    related_api.datamodel.model_name),
                'foreign_key': foreign_key,
                'type': relation_type,
                "path": related_api.resource_name + '/' or type(related_api).__name__ + '/'}

            relations.append(relation)

        response["relations"] = relations

    def merge_search_filters(self, response, **kwargs):
        """
        Overrides parent method to add the schema of a filter to the response. Selection is based on show columns.
        :param response: The response object
        :param kwargs: api endpoint kwargs
        """

        # Get possible search fields and all possible operations
        search_filters = dict()
        dict_filters = self._filters.get_search_filters()

        # TODO: this is bugged - since there is no schema for search_columns, search_colums must be a subset of show_columns
        for col in self.search_columns:
            search_filters[col] = {'label': self.label_columns[col], 'filters': [
                {"name": as_unicode(flt.name), "operator": flt.arg_name,
                 }
                for flt in dict_filters[col]
            ]}
            # Add schema info
            search_filters[col]['schema'] = self._get_field_info(self.search_model_schema.fields[col],
                                                                 self.search_query_rel_fields)
        response[API_FILTERS_RES_KEY] = search_filters

    def merge_quick_filters(self, response, **kwargs):
        """
        Overrides parent method to add the schema of a filter to the response. Selection is based on show columns.
        :param response: The response object
        :param kwargs: api endpoint kwargs
        """

        # Get possible search fields and all possible operations
        quick_filters = deepcopy(self.quick_filters)
        for qf in quick_filters or []:
            if callable(qf["options"]):
                qf["options"] = qf["options"]()

        response["quickfilters"] = quick_filters

    def merge_filter_options(self, response, **kwargs):
        """
        Overrides parent method to add the schema of a filter to the response. Selection is based on show columns.
        :param response: The response object
        :param kwargs: api endpoint kwargs
        """

        # Get possible search fields and all possible operations
        filter_options = deepcopy(self.filter_options)
        for k, v in filter_options.items() or {}.items():
            if callable(v):
                filter_options[k] = v()

        response["filter_options"] = filter_options

    @expose("/_info", methods=["GET"])
    @protect()
    @safe
    @rison(get_info_schema)
    @permission_name("info")
    @merge_response_func(
        BaseApi.merge_current_user_permissions, API_PERMISSIONS_RIS_KEY
    )
    @merge_response_func(ModelRestApi.merge_add_field_info, API_ADD_COLUMNS_RIS_KEY)
    @merge_response_func(ModelRestApi.merge_edit_field_info, API_EDIT_COLUMNS_RIS_KEY)
    @merge_response_func(merge_search_filters, API_FILTERS_RIS_KEY)
    @merge_response_func(ModelRestApi.merge_add_title, API_ADD_TITLE_RIS_KEY)
    @merge_response_func(ModelRestApi.merge_edit_title, API_EDIT_TITLE_RIS_KEY)
    @merge_response_func(merge_relations_info, "relations")
    @merge_response_func(merge_quick_filters, "quickfilters")
    @merge_response_func(merge_filter_options, "filter_options")
    def info(self, **kwargs):
        """ Endpoint that renders a response for CRUD REST meta data
        ---
        get:
          description: >-
            Get metadata information about this API resource
          parameters:
          - in: query
            name: q
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/get_info_schema'
          responses:
            200:
              description: Item from Model
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      add_columns:
                        type: object
                      edit_columns:
                        type: object
                      filters:
                        type: object
                        properties:
                          column_name:
                            type: array
                            items:
                              type: object
                              properties:
                                name:
                                  description: >-
                                    The filter name. Will be translated by babel
                                  type: string
                                operator:
                                  description: >-
                                    The filter operation key to use on list filters
                                  type: string
                      permissions:
                        description: The user permissions for this API resource
                        type: array
                        items:
                          type: string
            400:
              $ref: '#/components/responses/400'
            401:
              $ref: '#/components/responses/401'
            422:
              $ref: '#/components/responses/422'
            500:
              $ref: '#/components/responses/500'
        """
        return self.info_headless(**kwargs)




    @expose("/", methods=["GET"])
    @protect()
    @safe
    @permission_name("get")
    @better_rison(get_list_schema)
    @merge_response_func(ModelRestApi.merge_order_columns, API_ORDER_COLUMNS_RIS_KEY)
    @merge_response_func(ModelRestApi.merge_list_label_columns, API_LABEL_COLUMNS_RIS_KEY)
    @merge_response_func(ModelRestApi.merge_description_columns, API_DESCRIPTION_COLUMNS_RIS_KEY)
    @merge_response_func(ModelRestApi.merge_list_columns, API_LIST_COLUMNS_RIS_KEY)
    @merge_response_func(ModelRestApi.merge_list_title, API_LIST_TITLE_RIS_KEY)
    def get_list(self, **kwargs: Any) -> Response:
        """Get list of items from Model
        ---
        get:
          description: >-
            Get a list of models
          parameters:
          - in: query
            name: q
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/get_list_schema'
          responses:
            200:
              description: Items from Model
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      label_columns:
                        type: object
                        properties:
                          column_name:
                            description: >-
                              The label for the column name.
                              Will be translated by babel
                            example: A Nice label for the column
                            type: string
                      list_columns:
                        description: >-
                          A list of columns
                        type: array
                        items:
                          type: string
                      description_columns:
                        type: object
                        properties:
                          column_name:
                            description: >-
                              The description for the column name.
                              Will be translated by babel
                            example: A Nice description for the column
                            type: string
                      list_title:
                        description: >-
                          A title to render.
                          Will be translated by babel
                        example: List Items
                        type: string
                      ids:
                        description: >-
                          A list of item ids, useful when you don't know the column id
                        type: array
                        items:
                          type: string
                      count:
                        description: >-
                          The total record count on the backend
                        type: number
                      order_columns:
                        description: >-
                          A list of allowed columns to sort
                        type: array
                        items:
                          type: string
                      result:
                        description: >-
                          The result from the get list query
                        type: array
                        items:
                          $ref: '#/components/schemas/{{self.__class__.__name__}}.get_list'  # noqa
            400:
              $ref: '#/components/responses/400'
            401:
              $ref: '#/components/responses/401'
            422:
              $ref: '#/components/responses/422'
            500:
              $ref: '#/components/responses/500'
        """

        return self.get_list_headless(**kwargs)
