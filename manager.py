from typing import Dict
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
    
    def parseInput(self,selectable_options, userInput):
        quit = os.getenv('QUIT_COMMAND')
        if userInput == quit:
            self.router('/')
        else:
            self.router(selectable_options[int(userInput) - 1]['route'])
    
    def add_route(self, route, view):
        self.route_map[route] = view
