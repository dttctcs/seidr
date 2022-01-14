from flask_appbuilder import BaseView, expose
from . import appbuilder, db


class ReactView(BaseView):
    route_base = "/"

    @expose("/<string:path>")
    def react(self, path):
        return self.render_template("index.html")


appbuilder.add_view_no_menu(
    ReactView,
    "ReactView",
)

db.create_all()
