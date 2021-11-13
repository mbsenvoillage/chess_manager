from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Optional
import os
from manager import Router, ViewManager
from settings_loader import get_default_form_layout, get_default_page_layout, get_exit_route, get_quit_command
import readline


def get_page_layout(view):
    return get_default_form_layout() if isinstance(view, Form) else get_default_page_layout()

@dataclass
class View(ABC):
    """View parent class"""
    name: str
    title: str 
    info: List[str]  
    _router: Router
    _page_layout: str
 
    def __init__(self, name, router, title, info) -> None:
        super().__init__()
        self.name = name
        self._router = router
        self.title = title
        self.info = info

    def render(self):
        self._clear_terminal()
        self.print_content_to_screen()   
        self.handle_user_input()

    @abstractmethod
    def handle_user_input(self):
        pass

    @abstractmethod
    def format_view_content(self) -> str:
        pass

    def print_content_to_screen(self):
        print(self.format_view_content())

    def redirect_to(self,route):
        self._router.route(route)

    def concatenate_with(self,elements_to_display: List[str], concatenator):
        return concatenator.join(elements_to_display)

    def _clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'reset')

class MenuOption():
    text: str
    route: str

    def __init__(self, text, route) -> None:
        self.text = text
        self.route = route

class Menu(View):

    options: List[MenuOption]

    def __init__(self, name, router, title, info, options) -> None:
        super().__init__(name, router, title, info)
        self.options = []
        for option in options:
            self.options.append(MenuOption(text=option[0], route=option[1]))
        self._page_layout = get_page_layout(self)
          
    def handle_user_input(self):
        selected_option = input()
        requested_route = ''
        if selected_option == get_quit_command():
            requested_route = get_exit_route()
        else:
            requested_route = self.options[int(selected_option) - 1].route
        self.redirect_to(requested_route)

    def format_view_content(self) -> str:
        info = super().concatenate_with(self.info,"\n")
        options = super().concatenate_with([option.text for option in self.options],"\n")
        return self._page_layout.format(self.title, info, options)

class FormField():
    text: str
    type: str
    options: list[str]

    def __init__(self, text, type, options = []) -> None:
        self.text = text
        self.type = type
        self.options = options
        
class Completer(object):
    type_of_field_to_complete: str
    
    def __init__(self, options, type_of_field_to_complete):
        self.options = sorted(options)
        self.type_of_field_to_complete = type_of_field_to_complete
        return

    def complete(self, text, state):        
        response = None
        if state == 0:
            if text:
                self.matches = [s for s in self.options if s and s.startswith(text)]               
            else:
                self.matches = self.options
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response
class Form(View):

    form_fields: List[FormField]
    view_manager: ViewManager
    completer: Optional[Completer]

    def __init__(self, name, router, title, info, form_fields, view_manager, completer = None) -> None:
        super().__init__(name, router, title, info)
        self.form_fields = []
        for field in form_fields:
            self.form_fields.append(FormField(text=field[0], type=field[1]))
        self._page_layout = get_page_layout(self)
        self.view_manager = view_manager
        self.completer = completer

    def handle_user_input(self):
        inputs = []
        for field in self.form_fields:
            if self.completer is not None and field.type == self.completer.type_of_field_to_complete:
                    readline.set_completer(self.completer.complete)
                    readline.parse_and_bind('tab: complete')
            user_input = ''
            is_input_valid = False
            while not is_input_valid:    
                user_input = input(field.text)
                is_input_valid = self.is_valid(user_input, field.type)
                if not is_input_valid:
                    print("Submitted data is incorrect. Please enter valid data.")
            inputs.append(user_input)
        send_data = input('Do you want to add the data to the database ? (yes/no) ')
        if send_data == 'yes':
            self.submit_data(inputs)
        self.redirect_to('/')

    def format_view_content(self) -> str:
        info = super().concatenate_with(self.info,"\n")
        return self._page_layout.format(self.title, info)

    def submit_data(self,*data):
        self.view_manager.send(self.name,*data)

    def is_valid(self, user_input, field_type):
        return self.view_manager.validate(self.name, user_input, field_type)

           
class FormEdit(Form):
    data_id: str = ''

    def __call__(self, data : dict, id) -> None:
        self.data_id = id
        self.edit_form_fields(data)
        return self

    def edit_form_fields(self,data):
        for field in self.form_fields:
            key = field.type
            value = data[key]
            original_field_text = field.text
            field.text = f"{original_field_text}{value}\nNew value : "
     
    def handle_user_input(self):
        inputs = {}
        for field in self.form_fields:
            user_input = input(field.text)
            if user_input == '':
                continue
            is_input_valid = self.is_valid(user_input, field.type)
            while not is_input_valid:
                print("Submitted data is incorrect. Please enter valid data.")
                user_input = input(field.text)
                is_input_valid = self.is_valid(user_input, field.type)
            inputs[field.type] = user_input
        data_is_to_be_edited = input('Do you want to continue with this update ? (answer by yes or no) ')
        if data_is_to_be_edited == 'yes':
            self.submit_data(inputs, self.data_id)
        self.redirect_to('/player/edit/menu')