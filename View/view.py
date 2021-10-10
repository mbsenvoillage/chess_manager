from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List
from manager import ViewManager
import os

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
    prompt: str
    _view_manager: ViewManager
 
    def __init__(self, view_manager, content_loader, key: str) -> None:
        super().__init__()
        # attributes have to be initialized here since get_own_attributes cannot list uninitialized attributes (dir() does not offer the possibility)
        self.title = ''
        self.info = []
        self.selectable_options = []
        self.prompt = ''
        self._view_manager = view_manager
        content_loader.load_content(self, key)

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

    def capture_input():
        pass

    @abstractmethod
    def display_title(self):
        print('\n \n \t \t' + self.title)

    @abstractmethod
    def display_info(self):
        pass
        
    @abstractmethod
    def display_selectable_options(self):
        print('\n')
        for item in self.selectable_options:
            print(item['text'])
    
    @abstractmethod
    def display_prompt(self):
        return '\n' + self.prompt + ' '


class Menu(View):
    
    def submit(self, route):
            self._view_manager.router(route)

    def render(self):
        os.system('cls' if os.name == 'nt' else 'reset')
        self.display_title()
        self.display_info()
        self.display_selectable_options()
        self.submit(self.capture_input(self.display_prompt()))

    def display_title(self):
        return super().display_title()

    def display_info(self):
        print('\n')
        for item in self.info:
            print(item)
    
    def display_selectable_options(self):
        return super().display_selectable_options()

    def display_prompt(self):
        return super().display_prompt()
    
    def capture_input(self, prompt):
        selected_option = input(prompt)
        if selected_option == 'q':
            self._view_manager.router('/')
        else:
            to_submit = self.selectable_options[int(selected_option) - 1]['route']
        return to_submit
