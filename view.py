from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from manager import ViewManager
from store import static_view_content, app_data
import os
import re

class SelectableViewOptionBuilder():
    template: str
    store_data_key: str
    base_route: str
    displayables: List = []

    def __init__(self, template, store_data_key, base_route) -> None:
        self.template = template
        self.store_data_key = store_data_key
        self.base_route = base_route
        self.app_data_to_displayable_text()

    def app_data_to_displayable_text(self):
        """Formats content with template from data store to transform it into displayable text"""
        object_attributes = list(filter(None, re.split('\W+', self.template)))
        for item in app_data[self.store_data_key]:
            template_variables = {a: getattr(item, a) for a in object_attributes}
            self.displayables.append(self.template.format(**template_variables))
        return
        
    def build_view_options(self):
        """Builds view options"""
        view_options = []
        for option in self.displayables:
            view_options.append(ViewOption(option, self.base_route).make_option_dict())
        return view_options
            

class ViewContentLoader:
    """Loads content from data store into instance of view"""
    static_content: Dict = static_view_content
    app_data: Dict = app_data
    
    def plug_option_builder(self, builder, view_entry_to_populate):
        self.__setattr__('option_builder', builder)
        self.__setattr__('view_entry_to_populate', view_entry_to_populate)
        return self

    def unplug_option_builder(self):
        self.__delattr__('option_builder')
        self.__delattr__('view_entry_to_populate')

    def load_content(self, view, key: str):
        for attr in view.get_own_attributes():
                setattr(view, attr, self.static_content[key][attr])
        if hasattr(self, 'option_builder'):
            setattr(view, self.view_entry_to_populate, self.option_builder.build_view_options())
            self.unplug_option_builder()
        return 

@dataclass
class ViewOption(ABC):
    text: str
    route: str

    def make_option_dict(self):
        """Returns key/value representation of class where each class attribute is a key"""
        return self.__dict__

@dataclass
class View(ABC):
    """View parent class"""
    title: str 
    info: List[str] 
    main: List[ViewOption]
    prompt: str
    _view_manager: ViewManager
 
    def __init__(self, view_manager: ViewManager, content_loader: ViewContentLoader, key: str) -> None:
        super().__init__()
        # attributes have to be initialized here since get_own_attributes cannot list uninitialized attributes (dir() does not offer the possibility)
        self.title = ''
        self.info = []
        self.main = []
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
        if selected_option == 'q':
            self._view_manager.router('/')
        else:
            to_submit = self.main[int(selected_option) - 1]['route']
        return to_submit


print({} == None)