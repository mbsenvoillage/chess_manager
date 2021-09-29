from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Dict, List 
from store import view_data
import os



@dataclass
class View(ABC):
    title: str
    info: List[str]
    main: Dict
    prompt: str

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def submit(self, input_type, manager):
        pass

    @abstractmethod
    def load_content(self):
        pass

    @abstractmethod
    def display_title(self):
        print('\n \n \t \t' + self.title)

    @abstractmethod
    def display_info(self):
        print('\n')
        for item in self.info:
            print(item)
        
    @abstractmethod
    def display_main(self):
        print('\n')
        for attr,value in self.main.items():
            print(value['text'])
    
    @abstractmethod
    def display_prompt(self):
        print('\n' + self.prompt + '\n')


class Menu(View):

    def __init__(self, view_data, key) -> None:
        super().__init__()
        self.key = key
        self.load_content(view_data[self.key])
        

    def load_content(self, content):
        self.title = content['title']
        self.info = content['info']
        self.main = content['main']
        self.prompt = content['prompt']

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
        return super().display_info()
    
    def display_main(self):
        return super().display_main()

    def display_prompt(self):
        return super().display_prompt()

menu = Menu(view_data, 'MAIN_MENU')

menu.render()