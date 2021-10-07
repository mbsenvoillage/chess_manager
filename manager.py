from typing import Dict
from abc import ABC
import validator
from view import ContentLoader, Menu

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
    
    route_map: Dict 

    def router(self,route):
        self.route_map[route].render()
