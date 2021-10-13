from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List
from dotenv import load_dotenv
import os
from manager import ViewManager

load_dotenv()

@dataclass
class ViewOption(ABC):
    text: str
    route: str

    def represent_self_as_dict(self):
        """Returns key/value representation of class where each class attribute is a key"""
        return self.__dict__

@dataclass
class FormField(ABC):
    text: str
    class_attribute: str

def get_page_layout(view):
    page_layout = os.getenv('DEFAULT_PAGE_LAYOUT')
    if isinstance(view, Form):
        page_layout = os.getenv('FORM_PAGE_LAYOUT')
    return page_layout

def view_selectable_options_formatter(options: List[ViewOption]):
    formatted_text = ''
    for option in options:
        formatted_text += option['text'] + '\n'
    return formatted_text

def view_info_formatter(pieces_of_info):
    formatted_text = ''
    for info in pieces_of_info:
        formatted_text += info + '\n'
    return formatted_text

def view_form_fields_formatter(form_fields):
    formatted_fields = ''
    for field in form_fields:
        formatted_fields += field + '\n'
    return formatted_fields

@dataclass
class View(ABC):
    """View parent class"""
    title: str 
    info: List[str]  
    _view_manager: ViewManager
    _page_layout: str
 
    def __init__(self, view_manager) -> None:
        super().__init__()
        # attributes have to be initialized here since get_own_attributes cannot list uninitialized attributes (dir() does not offer the possibility)
        self.title = ''
        self.info = []
        self._page_layout = ''
        self._view_manager = view_manager

    def get_own_attributes(self):
        """Lists attributes of the view instance"""
        return [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a)) and not a.startswith('_')]

    @abstractmethod
    def render(self):
        """Renders the view"""
        os.system('cls' if os.name == 'nt' else 'reset')

    @abstractmethod
    def submit():
        """Submits user input to manager"""
        pass

    def format_info(self, format_helper_func):
        return format_helper_func(self.info)
        
    
class Menu(View):

    selectable_options: List[ViewOption]

    def __init__(self, view_manager, content_loader, key_of_view_to_be_loaded_from_store: str) -> None:
        super().__init__(view_manager)
        self.selectable_options = []
        self._page_layout = get_page_layout(self)
        content_loader.load_content(self, key_of_view_to_be_loaded_from_store)
        
    def submit(self, selected_option):
            self._view_manager.selected_option_to_route(self.selectable_options,selected_option)

    def format_selectable_options(self, format_helper_func):
        return format_helper_func(self.selectable_options)

    def assembleDisplayableElements(self):
        formatted_info = self.format_info(view_info_formatter)
        formatted_options = self.format_selectable_options(view_selectable_options_formatter)
        return [self.title, formatted_info, formatted_options]

    def render(self):
        super().render()
        print(self._page_layout.format(*self.assembleDisplayableElements()))    
        selected_option = input()
        self.submit(selected_option)



    
class Form(View):

    form_fields: List[FormField]

    def __init__(self, view_manager, content_loader, key_of_view_to_be_loaded_from_store: str) -> None:
        super().__init__(view_manager)
        self._page_layout = get_page_layout(self)
        self.form_fields = []
        content_loader.load_content(self, key_of_view_to_be_loaded_from_store)

    def format_form_fields(self, format_helper_func):
        return format_helper_func(self.form_fields)

    def get_input_data_manager_validator_key(self, ):
        pass

    def capture_form_inputs(self):
        inputs = []
        for field in self.form_fields:
            userInput = input(field)
            inputs.append(userInput)
        print(inputs)

    def render(self):
        super().render()
        formatted_info = self.format_info(view_info_formatter)
        print(self._page_layout.format(self.title, formatted_info))    
        self.capture_form_inputs()
    
    def submit(self, userInput):
        print(userInput)
        