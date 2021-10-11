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
    selectable_options: List[ViewOption]
    _view_manager: ViewManager
    _page_layout: str = field(default=os.getenv('PAGE_LAYOUT'))
 
    def __init__(self, view_manager, content_loader, key_of_view_to_be_loaded_from_store: str) -> None:
        super().__init__()
        # attributes have to be initialized here since get_own_attributes cannot list uninitialized attributes (dir() does not offer the possibility)
        self.title = ''
        self.info = []
        self.selectable_options = []
        self._view_manager = view_manager
        content_loader.load_content(self, key_of_view_to_be_loaded_from_store)

    def get_own_attributes(self):
        """Lists attributes of the view instance"""
        return [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a)) and not a.startswith('_')]

    @abstractmethod
    def render(self):
        """Renders the view"""
        pass

    @abstractmethod
    def submit():
        """Submits user input to manager"""
        pass

    def format_info(self, format_helper_func):
        return format_helper_func(self.info)
        
    def format_selectable_options(self, format_helper_func):
        return format_helper_func(self.selectable_options)
    
class Menu(View):
    
    def submit(self, userInput):
            self._view_manager.parseInput(userInput)

    def render(self):
        os.system('cls' if os.name == 'nt' else 'reset')
        formatted_info = self.format_info(view_info_formatter)
        formatted_options = self.format_selectable_options(view_selectable_options_formatter)
        print(self._page_layout.format(self.title, formatted_info, formatted_options))    
        userInput = input()
        self.submit(userInput)
  