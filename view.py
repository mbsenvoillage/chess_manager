from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Dict, List 
from store import view_data
import os


class ContentLoader:
    """Loads view content from view data store"""
    content: Dict = view_data

    def load_content(self, view, key: str):
        if isinstance(view, Menu):
            for attr in view.get_own_attributes():
                setattr(view, attr, self.content[key][attr])
       

@dataclass
class View(ABC):
    """View parent class"""
    title: str 
    info: List[str] 
    main: Dict 
    prompt: str
 
    def __init__(self) -> None:
        super().__init__()
        # attributes have to be initialized here since get_own_attributes cannot list uninitialized attributes (dir() does not offer the possibility)
        self.title = ''
        self.info = []
        self.main = {}
        self.prompt = ''

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

    @abstractmethod
    def display_title(self):
        print('\n \n \t \t' + self.title)

    @abstractmethod
    def display_info(self):
        pass
        
    @abstractmethod
    def display_main(self):
        print('\n')
        for attr,value in self.main.items():
            print(value['text'])
    
    @abstractmethod
    def display_prompt(self):
        print('\n' + self.prompt + '\n')




class Menu(View):

    def __init__(self, content_loader: ContentLoader,key) -> None:
        super().__init__()
        content_loader.load_content(self, key)
        
    def submit(self, input_type, manager):
        return super().submit(input_type, manager)

    def render(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_title()
        self.display_info()
        self.display_main()
        self.display_prompt()

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



menu = Menu(ContentLoader(), 'MAIN_MENU')

print(menu)