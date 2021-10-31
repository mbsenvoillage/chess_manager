from os import name
import random
from typing import List, Optional
from uuid import uuid4
import uuid
from pydantic import BaseModel, validator, PositiveInt
from datetime import date
import copy
from enums import TimeControl
from player import Player, gen_list_of_players, gen_player

class Match(BaseModel):
    player_one: Player
    player_two: Player
    player_one_result: Optional[int]

class Round(BaseModel):
    name: str
    start_time: Optional[date]
    end_time: Optional[date]
    matches: List[Match]

    def repr_matches(self):
        for match in self.matches:
            print(f"{match.player_one.get_info()} vs {match.player_two.get_info()} : {'TBP' if match.player_one_result is None else match.player_one_result} - {'TBP' if match.player_one_result is None else 1 - match.player_one_result}")
        
def generate_round_results(round: Round):
    copyOfRound = copy.deepcopy(round)
    for match in copyOfRound.matches:
        match.player_one_result =[0,0.5,1][random.randint(0,2)]
    return copyOfRound

class Tournament(BaseModel):
    id: str = str(uuid.uuid4())
    name: str
    venue: str
    start_date: Optional[date]
    end_date: Optional[date]
    number_of_rounds: int = 4
    rounds: list[Round]
    players: list[Player]
    time_control: TimeControl
    comments: str = ''
    locked: bool = False

    def __init__(self, **data) -> None:
        super().__init__(**data)
    
    @validator('players')
    def is_number_of_players_even(cls, value):
        if len(value) % 2 != 0:
            raise ValueError('Number of participants should be even')
        return value
 
    @validator('players')
    def is_number_of_players_sufficient(cls, value):
        if len(value) < 8:
            raise ValueError('There should be at least eight participants for the tournament')
        return value

# tournament = Tournament(name="Arctic Chess",venue="Royal Palace of Norway",rounds=[],players=gen_list_of_players(7),time_control='Bullet')
# print(tournament)