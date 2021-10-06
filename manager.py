from typing import Dict
from abc import ABC
import validator

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
