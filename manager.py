from typing import Dict, List
from abc import ABC, abstractmethod
from player import Player
import validator
import os
from dotenv import load_dotenv
from store import app_data



load_dotenv()


class DataManager(ABC):

    validators: Dict

    def __init__(self) -> None:
        super().__init__()
          
    def validate(self, data_to_validate, validator_key):
        return self.validators[validator_key](data_to_validate)
    
    @abstractmethod
    def add(self, data):
        pass


class PlayerManager(DataManager):

    validators = validator.player_validators
    player_store: List = app_data['players']

    def add(self, data):
        print(data)
        new_player = Player(first_name=data[0], last_name=data[1], birthdate=data[2], gender=data[3], ranking=data[4])
        print(new_player)
        self.player_store.append(new_player)


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
