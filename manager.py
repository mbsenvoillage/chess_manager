from typing import Dict, List
from player import Player
from abc import ABC, abstractmethod
import validator
import store

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

    app_data: Dict = store.app_data

    def assemble_option_list(self, data_type):
        option_list = []
        if data_type == 'player':
            for player in self.app_data['players']:
                option_list.append(f"{player.id}. {player.first_name} {player.last_name}")
        return option_list

print(ViewManager().assemble_option_list('player'))