from typing import Dict, List
from abc import ABC
import validator
import os
from dotenv import load_dotenv



load_dotenv()


class DataManager(ABC):

    validators: Dict

    def __init__(self) -> None:
        super().__init__()
        
    def get_validator(self, key):
        return self.validators[key]


class PlayerManager(DataManager):

    validators = validator.player_validators

    def add_player():
        pass


class ViewManager():
    
    route_map: Dict = {}

    def router(self,route):
        if route == '/exit':
            self.route_map[route]()
        else:
            self.route_map[route].render()
    
    def selected_option_to_route(self, selectable_options, selected_option):
        quit = os.getenv('QUIT_COMMAND')
        print(selected_option)
        if selected_option == quit:
            self.router('/')
        else:
            self.router(selectable_options[int(selected_option) - 1]['route'])
    
    def add_route(self, route, view):
        self.route_map[route] = view
