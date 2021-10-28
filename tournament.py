import random
from typing import List, Optional
from pydantic import BaseModel, validator, PositiveInt
from datetime import date
import copy
from player import Player, gen_player

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