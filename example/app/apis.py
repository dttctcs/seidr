from app.models import Asset, Unit
from seidr.interfaces import SeidrApi, SQLAInterface
from app import appbuilder

class AssetApi(SeidrApi):
    resource_name = "assets"
    datamodel = SQLAInterface(Asset)
    description_columns = {
        'name': 'Name of the asset',
        'owner_id': 'ID of the asset owner',
        'owner': 'Owner of the asset',
        'date_time': 'Date time of the asset',
        'date': 'Date of the asset',
    }
    quick_filters = [
        {
            "name": "asset_name",
            "label": "Asset Name",
            "column": "name",
            "type": "multiselect",
            "options": [{"value": f"asset&{i}", "label": f"asset&{i}"} for i in range(10)]
        }
    ]


class UnitApi(SeidrApi):
    resource_name = "units"
    datamodel = SQLAInterface(Unit)
    description_columns = {
        'name': 'Name of the unit'
    }
    quick_filters = [
        {
            "name": "unit_name",
            "label": "Unit Name",
            "column": "name",
            "type": "multiselect",
            "options": [{"value": f"unit_{i}", "label": f"unit_{i}"} for i in range(10)]
        }
    ]

appbuilder.add_api(AssetApi)
appbuilder.add_api(UnitApi)
