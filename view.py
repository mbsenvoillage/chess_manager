from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from store import view_data, app_data
import os
class ContentLoader:
    """Loads view content from data store"""
    view_text_content: Dict = view_data
    view_app_data: Dict = app_data
    data_to_assemble: str

    def __init__(self, data_to_assemble=None) -> None:
        self.data_to_assemble = data_to_assemble

 
    def assemble_option_list(self, data_to_assemble):
        option_list = []
        if data_to_assemble == 'player':
            for player in self.view_app_data['players']:
                option_list.append({'text': f"{player.id}. {player.first_name} {player.last_name}", "route": '/player/edit'})
        else:
            for tournament in self.view_app_data['tournaments']:
                option_list.append(f"{tournament.id}. {tournament.venue}")  
        return option_list

    def load_content(self, view, key: str):
        for attr in view.get_own_attributes():
                setattr(view, attr, self.view_text_content[key][attr])
        if self.data_to_assemble is not None:
            setattr(view, 'main', self.assemble_option_list(self.data_to_assemble))
        return 
       

@dataclass
class View(ABC):
    """View parent class"""
    title: str 
    info: List[str] 
    main: List 
    prompt: str
    _view_manager: any
 
    def __init__(self, content_loader: ContentLoader,key) -> None:
        super().__init__()
        # attributes have to be initialized here since get_own_attributes cannot list uninitialized attributes (dir() does not offer the possibility)
        self.title = ''
        self.info = []
        self.main = []
        self.prompt = ''
        self._view_manager = ViewManager()
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
        
    #[TODO] a different implementation of this method should be given for menus displaying dynamic list of options
    @abstractmethod
    def display_main(self):
        print('\n')
        for item in self.main:
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
        self.display_main()
        self.submit(self.capture_input(self.display_prompt()))

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
    
    def capture_input(self, prompt):
        selected_option = input(prompt)
        to_submit = self.main[int(selected_option) - 1]['route']
        return to_submit


class ViewManager():
    
    route_map: Dict 

    def __init__(self) -> None:
        self.route_map = {'/player': Menu(ContentLoader(), 'PLAYER_MENU')}

    def router(self,route):
        self.map[route].render()