from dataclasses import field, dataclass
from pydantic import PrivateAttr
from abc import ABC, abstractmethod
import sys
from typing import List
from View.content_formatter import view_selectable_options_formatter, view_info_formatter
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
class View(ABC):
    """View parent class"""
    title: str 
    info: List[str]  
    _view_manager: ViewManager
    _page_layout: str = field(default=os.getenv('PAGE_LAYOUT'))
 
    def __init__(self, view_manager) -> None:
        super().__init__()
        # attributes have to be initialized here since get_own_attributes cannot list uninitialized attributes (dir() does not offer the possibility)
        self.title = ''
        self.info = []
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
        content_loader.load_content(self, key_of_view_to_be_loaded_from_store)

    def render(self):
        super().render()
        formatted_info = self.format_info(view_info_formatter)
        formatted_options = self.format_selectable_options(view_selectable_options_formatter)
        print(self._page_layout.format(self.title, formatted_info, formatted_options))    
        userInput = input()
        self.submit(userInput)

    
    def submit(self, userInput):
            self._view_manager.parseInput(userInput)

    def format_selectable_options(self, format_helper_func):
        return format_helper_func(self.selectable_options)

    

class Form(View):
    form_fields: List[ViewOption]


    def render(self):
        pass
        