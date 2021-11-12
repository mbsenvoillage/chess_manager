import re
from typing import Any, Dict, List
from abc import ABC, abstractmethod
import json
from player import Player
from tournament import Tournament
import validator
from dotenv import load_dotenv
from database import players, tournaments
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
        new_player = Player(id=id, first_name=data[0], last_name=data[1], birthdate=data[2], gender=data[3], ranking=int(data[4]))
        self.player_store.insert(json.loads(new_player.json()))
    
    def get_all(self) -> List[Player]:
        return [Player(**playerdata) for playerdata in self.player_store.all()]

    def make_option_list(self,option_base_route):
        option_list = []
        for index, player in enumerate(self.get_all()):
            option_list.append([f"{index+1}. {player.first_name} {player.last_name}", f"{option_base_route}{player.id}"])
        return option_list

    def update(self, data, player_id):
        self.player_store.update(data, where('id') == player_id)

    def get_by_id(self, player_id):
        return self.player_store.search(where('id') == player_id)[0]
    
    def get_ranking(self,player_id):
        return self.get_by_id(player_id)['ranking']

    def get_by_identity(self,last_name,first_name,birthdate,ranking):
        return self.player_store.search((where('first_name') == first_name) & (where('last_name') == last_name) & (where('ranking') == ranking) & (where('birthdate') == birthdate))
    
print(PlayerManager().get_ranking("cb803b0f-cffe-45ce-b01f-f49933bfa9bd"))


class TournamentManager(DataManager):
    validators = validator.tournament_validators
    tournament_store = tournaments
    player_manager: PlayerManager

    def __init__(self, player_manager) -> None:
        super().__init__()
        self.player_manager = player_manager

    def add(self, data):
        id = str(uuid.uuid4())
        player_identities = list(filter(bool,data[5].split(' / ')))
        players = []
        for identity in player_identities:
            query_words = list(filter(bool,identity.split(' ')))
            db_response = self.player_manager.get_by_identity(query_words[0], query_words[1], query_words[2], int(query_words[3]))[0]
            players.append(db_response)
        new_tournament = Tournament(id=id,name=data[0], venue=data[1], start_date=data[2], end_date=data[3], number_of_rounds=data[4],rounds=[],players=players,time_control=data[6],comments=data[7])
        self.tournament_store.insert(json.loads(new_tournament.json()))

    def update(self, data, tournament_id):
        self.tournament_store.update(data, where('id') == tournament_id)

    def get_all(self) -> List[Tournament]:
        tournaments = []
        players = []
        for tournament in self.tournament_store.all():
            for player in tournament['players']:
                players.append(Player(**player))
            
                
        #     tournaments.append(Tournament(**tournament))
        # return tournaments

    def get_by_id(self, tournament_id):
        return self.tournament_store.search(where('id') == tournament_id)[0]
    
    def make_option_list(self,option_base_route):
        option_list = []
        for index, tournament in enumerate(self.get_all()):
            option_list.append([f"{index+1}. {tournament.name} {tournament.venue}", f"{option_base_route}{tournament.id}"])
        return option_list
    
class ViewManager():
    views: Dict = {}

    def __call__(self, views) -> Any:
        self.views = views
        return self

    def get_view(self,view_name,params=None):
        if params:
            data = self.views[view_name]['manager'].get_by_id(params)
            view = self.views[view_name]['view']()
            view(data,params).render()
        elif view_name == 'exit':
            self.views[view_name]['view']()
        else:
            view = self.views[view_name]['view']()
            view.render()

    def send(self,view_name,*data):
        update_data = len(data) > 1
        user_input = data[0]
        if update_data:    
            id = data[1]
            self.views[view_name]['manager'].update(user_input,id)
        else:
            self.views[view_name]['manager'].add(user_input)

    def validate(self,view_name,user_input,field_type):
        return self.views[view_name]['manager'].validate(user_input,field_type)


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
            self.view_manager.get_view(view_name, param)
        else:
            view_name = self.get_view_name_from_route(route)
            self.view_manager.get_view(view_name)


print(TournamentManager(PlayerManager()).get_all())