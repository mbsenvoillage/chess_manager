from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Dict, List 
from store import view_data, app_data
import os
import manager



class ContentLoader:
    """Loads view content from data store"""
    view_text_content: Dict = view_data
    view_app_data: Dict = app_data

    def assemble_option_list(self, data_type):
        option_list = []
        if data_type == 'player':
            for player in self.app_data['players']:
                option_list.append(f"{player.id}. {player.first_name} {player.last_name}")
        return option_list

    def load_content(self, view, key: str, assembly_func=None) -> None:
        for attr in view.get_own_attributes():
                setattr(view, attr, self.view_text_content[key][attr])
        if assembly_func is not None:
            setattr(view, 'main', assembly_func())
        return 
       

@dataclass
class View(ABC):
    """View parent class"""
    title: str 
    info: List[str] 
    main: List 
    prompt: str
    _view_manager: manager.ViewManager
    _data_manager: manager.PlayerManager
 
    def __init__(self, data_manager) -> None:
        super().__init__()
        # attributes have to be initialized here since get_own_attributes cannot list uninitialized attributes (dir() does not offer the possibility)
        self.title = ''
        self.info = []
        self.main = []
        self.prompt = ''
        self._data_manager = data_manager
        self._view_manager = manager.ViewManager

    def get_own_attributes(self):
        """Lists attributes of the view instance"""
        return [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a)) and not a.startswith('_')]

    @abstractmethod
    def render(self):
        """Renders the view"""
        pass

    @abstractmethod
    def submit(self, input_type, manager):
        """Submits user input to manager"""
        pass

    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'reset')

    
    def capture_input(self, prompt):
        to_submit = input(prompt)
        print('You submitted ' + to_submit)
        return to_submit

    @abstractmethod
    def display_title(self):
        print('\n \n \t \t' + self.title)

    @abstractmethod
    def display_info(self):
        pass
        
    @abstractmethod
    def display_main(self):
        print('\n')
        for item in self.main:
            print(item['text'])
    
    @abstractmethod
    def display_prompt(self):
        return '\n' + self.prompt




class Menu(View):

    def __init__(self, data_manager, content_loader: ContentLoader,key) -> None:
        super().__init__(data_manager)
        content_loader.load_content(self, key)
        
    def submit(self, input_type, manager):
        return super().submit(input_type, manager)

    def render(self):
        self.clear_terminal()
        self.display_title()
        self.display_info()
        self.display_main()
        self.capture_input(self.display_prompt())

    def display_title(self):
        return super().display_title()

    def display_info(self):
        print('\n')
        for item in self.info:
            print(item)
    
    def display_main(self):
        return super().display_main()

    def display_prompt(self):
        return super().display_prompt()


menu = Menu(manager.PlayerManager(), ContentLoader(), 'MAIN_MENU')
menu.render()