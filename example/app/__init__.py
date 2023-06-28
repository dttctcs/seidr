import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA, IndexView
from flask_cors import CORS
from flask_migrate import Migrate
from seidr import Seidr
from seidr.views import SeidrIndexView
import app.config

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
cors = CORS(app, supports_credentials=True, origins=["*"])

app.config.from_object(config)

db = SQLA(app)
migrate = Migrate(app, db)

index = SeidrIndexView if app.config.get("WEBAPP") else IndexView

appbuilder = AppBuilder(app=app, session=db.session, indexview=index)
seidr = Seidr(appbuilder)

from . import  apis
