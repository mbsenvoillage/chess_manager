from typing import Dict, List
from player import Player
from abc import ABC, abstractmethod
import validator

class Manager(ABC):

    validators: Dict

    def __init__(self) -> None:
        super().__init__()
        

    def get_validator(self, key):
        return self.validators[key]


class PlayerManager(Manager):

    validators = validator.player_validators

    def add_player():
        pass

manager = PlayerManager()

manager.get_validator('name')('michael')