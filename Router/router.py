import re
class Router():
    # view_manager: ViewManager
    route_map: dict = {}

    # def __init__(self, view_manager) -> None:
    #     self.view_manager = view_manager

    def add_route(self,route,controller):
        self.route_map[route] = controller
    
    def get_route(self, route: str, params):
        self.route_map[route](params)

    def get_url_param(self, route):
        import re
        return re.split('/|=|\?',route)[-1]

    def get_view_name_from_route(self, route):
        return '_'.join(list(filter(bool, re.match("((\/[a-z]*)+)", route).group().split('/'))))

    def start(self):
        self.route_map['/']()

    def route(self, route):
        params = None
        if "?" in route:
            params = self.get_url_param(route)
            # view_name = self.get_view_name_from_route(route)
            # self.view_manager.get_view(view_name, param)
        else:
            # view_name = self.get_view_name_from_route(route)
            # self.view_manager.get_view(view_name)
            self.get_route(route,params)
