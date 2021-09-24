from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, validator, PositiveInt
from pydantic.types import constr
from enums import Gender
from dateutil.relativedelta import relativedelta
import re







class Player(BaseModel):
    id: PositiveInt
    # [TODO] first name must not contain more than 25 letters and less than 2
    # may contain spaces, accents, dashes
    # may not contain numbers, special charactersc
    first_name: constr(strip_whitespace=True, min_length=2, max_length=25)
    last_name: constr(strip_whitespace=True, min_length=2, max_length=25)
    #players must be at least 6
    birthdate: date
    ranking: PositiveInt
    gender: Gender

    @validator('birthdate')
    def player_must_be_at_least_six(cls, value):
        if value > (date.today() - relativedelta(years=6)):
            raise ValueError('Player must be at least six years old')
        return value


    


print(Player(id=2, first_name='John90àç', last_name='Doe', birthdate='2018-03-30', ranking=2789, gender=Gender.Male))

