from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Optional, Union
import os
from Router.router import Router
from settings_loader import get_default_form_layout, get_default_page_layout, get_exit_route, get_quit_command
import readline
from prettytable import PrettyTable



def get_page_layout(view):
    return get_default_form_layout() if isinstance(view, Form) else get_default_page_layout()

@dataclass
class View(ABC):
    """View parent class"""
    from Controllers.controllers import Controller, FormController
    title: str 
    info: List[str]  
    controller: Union[Controller, FormController]
    page_layout: str
 
    def __init__(self, controller, page_layout, title, info) -> None:
        super().__init__()
        self.controller = controller
        self.title = title
        self.info = info
        self.page_layout = page_layout

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
        self.controller.redirect_to(route)

    def concatenate_with(self,elements_to_display: List[str], concatenator: str):
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

    def __init__(self, controller, page_layout, title, info, options) -> None:
        super().__init__(controller, page_layout, title, info)
        self.options = []
        for option in options:
            self.options.append(MenuOption(text=option[0], route=option[1]))

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
        return self.page_layout.format(self.title, info, options)

class ExitPage(View):

    def handle_user_input(self):
        selected_option = input()
        requested_route = ''
        if selected_option == 'yes':
            self.controller.exit()
        else:
            self.redirect_to(requested_route)

    def format_view_content(self) -> str:
        info = super().concatenate_with(self.info,"\n")
        return self.page_layout.format(self.title, info)


class FormField():
    text: str
    type: str
    options: Optional[list[str]]

    def __init__(self, text, type, options = []) -> None:
        self.text = text
        self.type = type
        self.options = options

class Report(Menu):

    search_results: list[str]
    table_headers: list

    def __init__(self, controller, page_layout, title, info, options,search_results,table_headers) -> None:
        super().__init__(controller, page_layout, title, info, options)
        self.search_results = search_results
        self.table_headers = table_headers

    def build_table(self):
        x = PrettyTable()
        x.field_names = self.table_headers
        for result in self.search_results:
            x.add_row(result)
        return x

    def handle_user_input(self):
        selected_option = input()
        requested_route = ''
        if selected_option == get_quit_command():
            requested_route = get_exit_route()
            self.redirect_to(requested_route)
        else:
            search_criteria = self.options[int(selected_option) - 1].route
            self.controller.search(search_criteria)
        

    def format_view_content(self) -> str:
        info = super().concatenate_with(self.info,"\n")
        options = super().concatenate_with([option.text for option in self.options],"\n")
        return self.page_layout.format(self.title, info, self.build_table(),options)

        
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
    completer: Optional[Completer]

    def __init__(self, controller, page_layout, title, info, form_fields, completer = None) -> None:
        super().__init__(controller, page_layout, title, info)
        self.form_fields = []
        if form_fields: 
            for field in form_fields:
                self.form_fields.append(FormField(text=field[0], type=field[1]))
        self.page_layout = page_layout
        self.completer = completer

    def handle_user_input(self):
        inputs = {}
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
            inputs[field.type] = user_input
        send_data = input('Do you want to add the data to the database ? (yes/no) ')
        if send_data == 'yes':
            self.submit_data(inputs)
        self.redirect_to('/')

    def format_view_content(self) -> str:
        info = super().concatenate_with(self.info,"\n")
        return self.page_layout.format(self.title, info)

    def submit_data(self,inputs: dict):
        self.controller.submit(inputs)

    def is_valid(self, user_input, field_type) -> bool:
        return self.controller.validate_input(user_input, field_type)

           
class FormEdit(Form):
     
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
            self.submit_data(inputs)
        self.redirect_to('/player/edit/menu')