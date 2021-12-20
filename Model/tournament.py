from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
from Model.enums import TimeControl
from dateutil import parser
from dateutil.relativedelta import relativedelta


class Match(BaseModel):
    player_one: str
    player_two: str
    player_one_result: Optional[int]


class Round(BaseModel):
    name: str
    start_time: Optional[date]
    end_time: Optional[date]
    matches: List[Match]


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

    @validator('name')
    def name_validator(cls, value):
        import re
        regex = re.compile("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$")
        if not (regex.match(value) and len(value) > 2 and len(value) < 100):
            raise ValueError('Name should be no longer than 100 characters and contain alpha characters only')
        return value

    @validator('venue')
    def venue_validator(cls, value):
        import re
        regex = re.compile("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$")
        if not (regex.match(value) and len(value) > 2 and len(value) < 100):
            raise ValueError('The venue name should be no longer than 100 characters and contain alpha characters only')
        return value
    
    @validator('start_date')
    def start_date_validator(cls, value):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if not (parser.parse(f'{value} {current_time}') >= (datetime.now() - relativedelta(hours=1))):
            raise ValueError('The start date should be posterior to this moment minus an hour')
        return value

    @validator('end_date')
    def end_date_validator(cls, value, values):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if not (parser.parse(f'{value} {current_time}') >= (parser.parse(f"{values['start_date']} {current_time}"))):
            raise ValueError('The end date should be posterior to the start date')
        return value

    @validator('number_of_rounds')
    def num_of_rounds_validator(cls, value):
        if not (value >= 4):
            raise ValueError("There must be at least four rounds")
        return value
    
    @validator('players')
    def players_validator(cls, value):
        if not (len(value) >= 8):
            raise ValueError("There must be at least eight players")
        return value
