from seidr.apis import AuthApi, InfoApi

class Seidr(object):

    def __init__(self, appbuilder):
        self.appbuilder = appbuilder
        self.appbuilder.seidr = self
        self.appbuilder.app.config.setdefault("SEIDR_AUTH", True)
        self.appbuilder.app.config.setdefault("SEIDR_INFO", True)
        
        if self.appbuilder.app.config.get("SEIDR_AUTH"):
            self.appbuilder.add_api(AuthApi)
        if self.appbuilder.app.config.get("SEIDR_INFO"):
            self.appbuilder.add_api(InfoApi)

