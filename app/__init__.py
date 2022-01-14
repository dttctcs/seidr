import logging

from flask import Flask
from flask_cors import CORS
from flask_appbuilder import AppBuilder, SQLA, IndexView


#  Create custom index view
class MyIndexView(IndexView):
    index_template = 'index.html'


"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
cors = CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://localhost:5000"])
app.config.from_object("config")
db = SQLA(app)

appbuilder = AppBuilder(app, db.session, indexview=MyIndexView)

# this is to be able to access "appbuilder" api
from . import api

db.create_all()
