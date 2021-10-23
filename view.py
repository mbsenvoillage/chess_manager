from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import time
from typing import List
from dotenv import load_dotenv
import os
from manager import DataManager, Router


load_dotenv()

def get_page_layout(view):
    return os.getenv('DEFAULT_FORM_LAYOUT') if isinstance(view, Form) else os.getenv('DEFAULT_PAGE_LAYOUT')

@dataclass
class View(ABC):
    """View parent class"""
    title: str 
    info: List[str]  
    _router: Router
    _page_layout: str
 
    def __init__(self, router, title, info) -> None:
        super().__init__()
        self._router = router
        self.title = title
        self.info = info

    def render(self):
        os.system('cls' if os.name == 'nt' else 'reset')
        print(self.format_view_content())    
        self.handle_user_input()

    @abstractmethod
    def submit():
        pass

    @abstractmethod
    def handle_user_input(self):
        pass

    @abstractmethod
    def format_view_content(self) -> str:
        pass

    def get_string_repr(self,elements_to_display: List[str]):
        return "\n".join(elements_to_display)

class Menu(View):

    options: List[List[str]]

    def __init__(self, router, title, info, options) -> None:
        super().__init__(router, title, info)
        self.options = options
        self._page_layout = get_page_layout(self)

    def submit(self, selected_option):
        if selected_option == os.getenv('QUIT_COMMAND'):
            self._router.route(os.getenv('QUIT_REDIRECTION_ROUTE'))
        else:
            self._router.route(self.options[int(selected_option) - 1][1])
             
    def handle_user_input(self):
        self.submit(input())

    def format_view_content(self) -> str:
        info = super().get_string_repr(self.info)
        options = super().get_string_repr([option[0] for option in self.options])
        return self._page_layout.format(self.title, info, options)

class Form(View):

    form_fields: List[List[str]]
    _data_manager: DataManager

    def __init__(self, router, title, info, form_fields, data_manager) -> None:
        super().__init__(router, title, info)
        self.form_fields = form_fields
        self._page_layout = get_page_layout(self)
        self._data_manager = data_manager

    def handle_user_input(self):
        inputs = []
        for field in self.form_fields:
            userInput = input(field[0])
            userInputIsValid = self._data_manager.validate(userInput, field[1])
            while not userInputIsValid:
                print("Submitted data is incorrect. Please enter valid data.")
                userInput = input(field[0])
                userInputIsValid = self._data_manager.validate(userInput, field[1])
            inputs.append(userInput)
        player_is_to_be_added = input('Do you want to add the player to the database ? (answer by yes or no) ')
        if player_is_to_be_added == 'yes':
            self._data_manager.add(inputs)
        self._router.route('/player/edit')

    def format_view_content(self) -> str:
        info = super().get_string_repr(self.info)
        return self._page_layout.format(self.title, info)
           
    def submit(self, userInput):
        print(userInput)

class FormEdit(Form):

    def __call__(self, data : dict, id) -> None:
        self.__setattr__('_data_store_id', id)
        for field in self.form_fields:
            key = field[1]
            value = data[key]
            original_field_text = field[0]
            new_field_text = f"{original_field_text}{value}\nNew value : "
            field[0] = new_field_text
        return self
        
    def handle_user_input(self):
        inputs = {}
        for field in self.form_fields:
            userInput = input(field[0])
            if userInput == '':
                continue
            userInputIsValid = self._data_manager.validate(userInput, field[1])
            while not userInputIsValid:
                print("Submitted data is incorrect. Please enter valid data.")
                userInput = input(field[0])
                userInputIsValid = self._data_manager.validate(userInput, field[1])
            inputs[field[1]] = userInput
        data_is_to_be_edited = input('Do you want to continue with this update ? (answer by yes or no) ')
        if data_is_to_be_edited == 'yes':
            self._data_manager.update(inputs, self.__getattribute__('_data_store_id'))
        self._router.route('/player/edit')