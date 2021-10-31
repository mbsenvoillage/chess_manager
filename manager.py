import re
from typing import Any, Dict, List
from abc import ABC, abstractmethod
import json
from player import Player
import validator
from dotenv import load_dotenv
from database import db, players
import uuid
from tinydb import where

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

    @abstractmethod
    def update(self, data, id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

class PlayerManager(DataManager):

    validators = validator.player_validators
    player_store = players

    def add(self, data):
        id = str(uuid.uuid4())
        new_player = Player(id=id, first_name=data[0], last_name=data[1], birthdate=data[2], gender=data[3], ranking=data[4])
        self.player_store.insert(json.loads(new_player.json()))
    
    def get_all(self) -> List[Player]:
        return [Player(**playerdata) for playerdata in players.all()]

    def make_option_list(self,option_base_route):
        option_list = []
        for index, player in enumerate(self.get_all()):
            option_list.append([f"{index+1}. {player.first_name} {player.last_name}", f"{option_base_route}{player.id}"])
        return option_list

    def update(self, data, player_id):
        self.player_store.update(data, where('id') == player_id)

    def get_by_id(self, player_id):
        return self.player_store.search(where('id') == player_id)[0]

class ViewManager():
    views: Dict

    def __init__(self, views) -> None:
        self.views = views

    def get(self,view_name,params=None):
        if params:
            data = self.views[view_name]['manager'].get_by_id(params)
            view = self.views[view_name]['view']()
            view(data,params).render()
        elif view_name == 'exit':
            self.views[view_name]['view']()
        else:
            print(self.views[view_name])
            view = self.views[view_name]['view']()
            view.render()


class Router():
    view_manager: ViewManager

    def __init__(self, view_manager) -> None:
        self.view_manager = view_manager

    def get_url_param(self, route):
        import re
        if 'player' in route:
            return re.split('/|=|\?',route)[-1]

    def get_view_name_from_route(self, route):
        return '_'.join(list(filter(bool, re.match("((\/[a-z]*)+)", route).group().split('/'))))

    def route(self, route):
        if "?" in route:
            param = self.get_url_param(route)
            view_name = self.get_view_name_from_route(route)
            self.view_manager.get(view_name, param)
        else:
            view_name = self.get_view_name_from_route(route)
            self.view_manager.get(view_name)

print('_'.join(list(filter(bool, re.match("((\/[a-z]*)+)", '/home/player/other?id=18').group().split('/')))))