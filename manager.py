import re
from typing import Any, Dict, List
from abc import ABC, abstractmethod
import json
from player import Player
import validator
from dotenv import load_dotenv
from store import app_data
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

class PlayerManager(DataManager):

    validators = validator.player_validators
    player_store = players

    def add(self, data):
        id = str(uuid.uuid4())
        new_player = Player(id=id, first_name=data[0], last_name=data[1], birthdate=data[2], gender=data[3], ranking=data[4])
        self.player_store.insert(json.loads(new_player.json()))
    
    def get_all_players(self) -> List[Player]:
        return [Player(**playerdata) for playerdata in players.all()]

    def make_option_list(self):
        option_list = []
        for index, player in enumerate(self.get_all_players()):
            option_list.append([f"{index+1}. {player.first_name} {player.last_name}", f"/player/edit?id={player.id}"])
        return option_list

    def update(self, data, player_id):
        self.player_store.update(data, where('id') == player_id)

    def get_player_by_id(self, player_id):
        return self.player_store.search(where('id') == player_id)[0]

class ViewManager():
    
    route_map: Dict = {}

    def router(self,route):
        if route == '/exit':
            self.route_map[route]()
        if "?" in route:
            self
        else:
            self.route_map[route].render()
      
    def add_route(self, route, view):
        self.route_map[route] = view


class Router():
    route_map: Dict = {}
    player_manager : PlayerManager

    def __init__(self, player_manager) -> None:
        self.player_manager = player_manager

    def __call__(self, routes) -> Any:
        for route in routes:
            self.route_map[route['path']] = route['view']

    def get_url_param(self, route):
        import re
        if 'player' in route:
            return re.split('/|=|\?',route)[-1]

    def get_base_url(self, route):
        return re.match("\/[a-z]*\/[a-z]*\?", route).group()

    def route(self, route):
        if route == '/exit':
            self.route_map[route]()
        if "?" in route:
            id = self.get_url_param(route)
            base_url = self.get_base_url(route)
            data = self.player_manager.get_player_by_id(id)
            view = self.route_map[base_url]()
            view(data,id).render()
        else:
            view =  self.route_map[route]()
            view.render()