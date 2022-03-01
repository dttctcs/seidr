from flask_appbuilder.api import BaseApi, ModelRestApi, merge_response_func, expose, safe, rison, get_info_schema
from flask_appbuilder._compat import as_unicode

from flask_appbuilder.security.decorators import permission_name, protect

from flask_appbuilder.const import API_ADD_COLUMNS_RIS_KEY, API_ADD_TITLE_RIS_KEY, API_PERMISSIONS_RIS_KEY, \
    API_EDIT_COLUMNS_RIS_KEY, API_FILTERS_RIS_KEY, API_EDIT_TITLE_RIS_KEY, API_FILTERS_RES_KEY

from seidr.interfaces.convert import Model2SchemaConverter


class BaseModelRestApi(ModelRestApi):
    related_apis = []
    """
        List with ModelRestApi classes
        Will add related_apis information to the info endpoint

            class MyApi(BaseModelRestApi):
                datamodel = SQLAModel(Group, db.session)
                related_apis = [MyOtherApi]

    """

    model2schemaconverter = Model2SchemaConverter

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
            relation = {'name': related_api.datamodel.model_name,
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
    
        for col in self.list_columns:
            search_filters[col] = {'filters': [
                {"name": as_unicode(flt.name), "operator": flt.arg_name,
                 }
                for flt in dict_filters[col]
            ]}
            # Add schema info
            search_filters[col]['schema'] = self._get_field_info(self.list_model_schema.fields[col],
                                                                 self.list_model_schema)
        response[API_FILTERS_RES_KEY] = search_filters

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
