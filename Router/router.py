import re
class Router():
    route_map: dict = {}

    def add_route(self,route,controller):
        self.route_map[route] = controller
    
    def get_route(self, route: str, params):
        self.route_map[route](params)

    def get_url_param(self, route):
        import re
        return re.split('/|=|\?',route)[-1]

    def start(self):
        self.route_map['/'](params=None)

    def route(self, route):
        params = None
        if "?" in route:
            params = self.get_url_param(route)
            route = re.match('.*\?',route)[0]
        self.get_route(route,params)
