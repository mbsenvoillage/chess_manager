from abc import ABC, abstractmethod
from typing import Union
from manager import DataManager, PlayerManager, TournamentManager
from Router.router import Router
from settings_loader import get_default_form_layout, get_default_page_layout
from store import static_view_content


class Controller(ABC):
    router: Router

    def __init__(self,router) -> None:
        super().__init__()
        self.router = router

    def __call__(self,params=None):
        return self.index(params)

    @abstractmethod
    def index(self,data):
        pass

    def redirect_to(self,route):
        self.router.route(route)
    
    @abstractmethod
    def validate_command(self,command):
        pass

class FormController(Controller):
    data_manager: Union[PlayerManager,TournamentManager]

    def __init__(self, router, data_manager) -> None:
        super().__init__(router)
        self.data_manager = data_manager

    @abstractmethod
    def index(self, data):
        pass
    
    @abstractmethod
    def validate_command(self, command):
        pass

    @abstractmethod
    def validate_input(self,input,field_type):
        pass

    @abstractmethod
    def submit(self,inputs):
        pass

class MainMenuContoller(Controller):
    
    def index(self,data):
        from view import Menu
        main_menu_content = static_view_content['MAIN_MENU']
        return Menu(self, get_default_page_layout(), *main_menu_content.values()).render()

    def validate_command(self, command):
        pass

class PlayerMenuController(Controller):
    
    def index(self, data):
        from view import Menu
        player_menu_content = static_view_content['PLAYER_MENU']
        return Menu(self, get_default_page_layout(), *player_menu_content.values()).render()

    def validate_command(self, command):
        pass

class CreatePlayerFormController(FormController):

    def index(self, data):
        from view import Form
        player_create_content = static_view_content['PLAYER_CREATE']
        return Form(self, get_default_form_layout(),*player_create_content.values()).render()
    def validate_command(self, command):
        pass

    def validate_input(self, input,field_type):
        return self.data_manager.validate(input,field_type)

    def submit(self, inputs):
        self.data_manager.add(inputs)
