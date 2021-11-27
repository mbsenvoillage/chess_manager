import re
from typing import Dict, List
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

    def update(self, data, player_id):
        if 'ranking' in data:
            ranking = int(data['ranking'])
            data['ranking'] = ranking
        self.player_store.update(data, where('id') == player_id)

    def get_by_id(self, player_id):
        return self.player_store.search(where('id') == player_id)[0]

    def get_by_identity(self,last_name,first_name,birthdate,ranking):
        return self.player_store.search((where('first_name') == first_name) & (where('last_name') == last_name) & (where('ranking') == ranking) & (where('birthdate') == birthdate))
    
    
class TournamentManager(DataManager):
    validators = validator.tournament_validators
    tournament_store = tournaments
    player_manager: PlayerManager

    def __init__(self, player_manager) -> None:
        super().__init__()
        self.player_manager = player_manager

    def add(self, data: dict) -> None:
        id = str(uuid.uuid4())
        player_identities = list(filter(bool,data['players'].split(' / ')))
        players = []
        for identity in player_identities:
            query_words = list(filter(bool,identity.split(' ')))
            db_response = self.player_manager.get_by_identity(query_words[0], query_words[1], query_words[2], int(query_words[3]))[0]
            players.append(db_response['id'])
        params = {
            'id': id,
            'name': data['name'],
            'venue': data['venue'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'number_of_rounds': data['number_of_rounds'],
            'rounds': [],
            'players': players,
            'time_control': data['time_control'],
            'comments': data['comments'],
            'leaderboard': matchmaker.init_leader_board(players)
        }
        new_tournament = Tournament(**params)
        new_tournament.rounds.append(matchmaker.make_round(new_tournament))
        self.tournament_store.insert(json.loads(new_tournament.json()))

    def update(self, data: dict, tournament_id: str) -> None:
        scores = list(data.values())
        tournament = Tournament(**self.get_by_id(tournament_id))
        players = [PlayerManager().get_by_id(id) for id in tournament.players]
        for idx, match in enumerate(tournament.rounds[-1].matches):
            score = 0.5 if scores[idx] == '0.5' else int(scores[idx])
            match.player_one_result = score
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


l = {'one': 1, 'two': 2, 'three': 3}

s = l.values()

print(list(s))