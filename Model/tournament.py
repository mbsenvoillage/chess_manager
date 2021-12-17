import random
from typing import List, Optional
from pydantic import BaseModel
from datetime import date
import copy
from Model.enums import TimeControl


class Match(BaseModel):
    player_one: str
    player_two: str
    player_one_result: Optional[int]


class Round(BaseModel):
    name: str
    start_time: Optional[date]
    end_time: Optional[date]
    matches: List[Match]


def generate_round_results(round: Round):
    copyOfRound = copy.deepcopy(round)
    for match in copyOfRound.matches:
        match.player_one_result = [0, 0.5, 1][random.randint(0, 2)]
    return copyOfRound


class Tournament(BaseModel):
    id: str
    name: str
    venue: str
    start_date: Optional[date]
    end_date: Optional[date]
    number_of_rounds: int = 4
    rounds: list[Round]
    players: list[str]
    time_control: TimeControl
    comments: str = ''
    leaderboard: dict = {}

    # @validator('players')
    # def is_number_of_players_even(cls, value):
    #     if len(value) % 2 != 0:
    #         raise ValueError('Number of participants should be even')
    #     return value

    # @validator('players')
    # def is_number_of_players_sufficient(cls, value):
    #     if len(value) < 8:
    #         raise ValueError('There should be at least eight participants for the tournament')
    #     return value
