from abc import ABC, abstractmethod
import copy
from typing import Union
from manager import PlayerManager, TournamentManager
from Router.router import Router
from settings_loader import get_default_form_layout, get_default_page_layout
from store import static_view_content


class Controller(ABC):
    router: Router
    data_manager: Union[PlayerManager,TournamentManager]
    data_id: str = None

    def __init__(self,router,data_manager=None) -> None:
        super().__init__()
        self.router = router
        self.data_manager = data_manager

    def __call__(self,params):
        if params:
            self.data_id = params
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

class EditPlayerMenuController(Controller):

    def index(self, data):
        from view import Menu
        edit_player_menu_content = static_view_content['PLAYER_EDIT_MENU']
        options = self.make_menu_options('/player/edit/form?id=')
        return Menu(self, get_default_page_layout(), *edit_player_menu_content.values(), options).render()

    def validate_command(self, command):
        pass

    def make_menu_options(self,base_route):
        list_of_options = []
        for index, player in enumerate(self.data_manager.get_all()):
            list_of_options.append([f"{index+1}. {player.first_name} {player.last_name}", f"{base_route}{player.id}"])
        return list_of_options

class EditPlayerFormController(FormController):

    def index(self,data):
        from view import FormEdit
        edit_player_form_content = static_view_content['PLAYER_EDIT_FORM']
        form = FormEdit(self, get_default_form_layout(), *edit_player_form_content.values())
        edited_form_fields = self.edit_form(self.data_manager.get_by_id(data),form.form_fields)
        form.form_fields = edited_form_fields
        return form.render()

    def validate_command(self, command):
        pass

    def validate_input(self, input,field_type):
        return self.data_manager.validate(input,field_type)

    def submit(self, inputs):
        self.data_manager.update(inputs,self.data_id)

    def edit_form(self,entity: dict,form_fields):
        fields = copy.deepcopy(form_fields)
        for field in fields:
            key = field.type
            value = entity[key]
            original_field_text = field.text
            field.text = f"{original_field_text}{value}\nNew value : "
        return fields