from datetime import date
import datetime
from typing import ClassVar, List, Optional
from pydantic import BaseModel, validator, PositiveInt
from pydantic.fields import PrivateAttr
from pydantic.types import constr
from enums import Gender
from dateutil.relativedelta import relativedelta
import itertools

class Player(BaseModel):
    _id_count = itertools.count(1)
    _id: PositiveInt = PrivateAttr()
    # [TODO] first name must not contain more than 25 letters and less than 2
    # may contain spaces, accents, dashes
    # may not contain numbers, special charactersc
    first_name: constr(strip_whitespace=True, min_length=2, max_length=25)
    last_name: constr(strip_whitespace=True, min_length=2, max_length=25)
    #players must be at least 6
    # [TODO] add date format hint for user (yyyy-mm-dd)
    birthdate: date
    ranking: PositiveInt
    gender: Gender


    @validator('birthdate')
    def player_must_be_at_least_six(cls, value):
        if value > (date.today() - relativedelta(years=6)):
            raise ValueError('Player must be at least six years old')
        return value


    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._id = next(Player._id_count)

    # Class's string representation
    def __repr__(self):
        return f"First name: {self.first_name} \nLast name: {self.last_name} \nGender: {self.gender.value} \nRanking: {self.ranking}\nBirthdate: {self.birthdate}"
    
# player1 = Player(first_name='John', last_name='Doe', birthdate='1989-10-04', ranking=2390, gender='M')
# player2 = Player(first_name='Peter', last_name='Callum', birthdate='1970-11-09', ranking=2790, gender='M')
# player3 = Player(first_name='Leila', last_name='Erviti', birthdate='1998-03-09', ranking=2890, gender='F')
# print(player2.json())
# print(player3.json())