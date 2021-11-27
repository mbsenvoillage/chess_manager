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
import matchmaker
import copy

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
        params = {
            'id': str(uuid.uuid4()), 
            'first_name': data['first_name'], 
            'last_name': data['last_name'], 
            'birthdate': data['birthdate'], 
            'gender': data['gender'], 
            'ranking': int(data['ranking'])
        }
        new_player = Player(**params)
        self.player_store.insert(json.loads(new_player.json()))
    
    def get_all(self,order_by: str = '') -> List[Player]:
        players = [Player(**playerdata) for playerdata in self.player_store.all()]
        if order_by == 'alpha':
            players.sort(key=lambda x: x.last_name)
        if order_by == 'ranking':
            players.sort(key=lambda x: x.ranking, reverse=True)    
        return players

    def make_option_list(self,option_base_route):
        option_list = []
        for index, player in enumerate(self.get_all()):
            option_list.append([f"{index+1}. {player.first_name} {player.last_name}", f"{option_base_route}{player.id}"])
        return option_list

    def update(self, data, player_id):
        if 'ranking' in data:
            ranking = int(data['ranking'])
            data['ranking'] = ranking
        self.player_store.update(data, where('id') == player_id)

    def get_by_id(self, player_id):
        return self.player_store.search(where('id') == player_id)[0]

    def get_by_identity(self,last_name,first_name,birthdate,ranking):
        return self.player_store.search((where('first_name') == first_name) & (where('last_name') == last_name) & (where('ranking') == ranking) & (where('birthdate') == birthdate))
    
    def make_form(self,entity: dict,form_fields):
        fields = copy.deepcopy(form_fields)
        for field in fields:
            key = field.type
            value = entity[key]
            original_field_text = field.text
            field.text = f"{original_field_text}{value}\nNew value : "
        return fields
    
class TournamentManager(DataManager):
    validators = validator.tournament_validators
    tournament_store = tournaments
    player_manager: PlayerManager

    def __init__(self, player_manager) -> None:
        super().__init__()
        self.player_manager = player_manager

    def add(self, data: dict) -> None:
        id = str(uuid.uuid4())
        player_identities = list(filter(bool,data[5].split(' / ')))
        players = []
        for identity in player_identities:
            query_words = list(filter(bool,identity.split(' ')))
            db_response = self.player_manager.get_by_identity(query_words[0], query_words[1], query_words[2], int(query_words[3]))[0]
            players.append(db_response['id'])
        params = {
            'id': id,
            'name': data[0],
            'venue': data[1],
            'start_date': data[2],
            'end_date': data[3],
            'number_of_rounds': data[4],
            'rounds': [],
            'players': players,
            'time_control': data[6],
            'comments': data[7],
            'leaderboard': matchmaker.init_leader_board(players)
        }
        new_tournament = Tournament(**params)
        round1 = matchmaker.make_round(new_tournament)
        new_tournament.rounds.append(round1)
        self.tournament_store.insert(json.loads(new_tournament.json()))

    def update(self, data: dict, tournament_id: str) -> None:
        scores = data
        tournament = Tournament(**self.get_by_id(tournament_id))
        players = [PlayerManager().get_by_id(id) for id in tournament.players]
        for idx, match in enumerate(tournament.rounds[-1].matches):
            match.player_one_result = int(scores[idx])
        updated_leaderboard = matchmaker.update_leaderboard(players,tournament)
        tournament.leaderboard = updated_leaderboard
        round = matchmaker.make_round(tournament)
        tournament.rounds.append(round)
        self.tournament_store.update(json.loads(tournament.json()), where('id') == tournament_id)
        
    def get_all(self) -> List[Tournament]:
        tournaments = []
        for tournament in self.tournament_store.all():         
            tournaments.append(Tournament(**tournament))
        return tournaments

    def get_by_id(self, tournament_id):
        return self.tournament_store.search(where('id') == tournament_id)[0]
    
    def make_option_list(self,option_base_route):
        option_list = []
        for index, tournament in enumerate(self.get_all()):
            option_list.append([f"{index+1}. {tournament.name} - Venue: {tournament.venue}", f"{option_base_route}{tournament.id}"])
        return option_list

    def make_form(self,entity: dict,form_fields = []):
        fields = []
        for match in entity['rounds'][-1]['matches']:
            field = {'type': 'match'}
            player_one = PlayerManager().get_by_id(match['player_one'])
            player_two = PlayerManager().get_by_id(match['player_two'])
            text = f"{player_one['first_name']} {player_one['last_name']} vs {player_two['first_name']} {player_two['last_name']}\n{player_one['first_name']} {player_one['last_name']}'s score : "
            field['text'] = text
            fields.append(field)
        return fields
    
class ViewManager():
    views: Dict = {}

    def __call__(self, views) -> Any:
        self.views = views
        return self

    def get_view(self,view_name,params=None):
        if params:
            entity = self.views[view_name]['manager'].get_by_id(params)
            view = self.views[view_name]['view']()
            make_form_params = [entity]
            if view.form_fields:
                make_form_params.append(view.form_fields)
            data = self.views[view_name]['manager'].make_form(*make_form_params)
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
