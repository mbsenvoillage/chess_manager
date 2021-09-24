from datetime import date, datetime
from typing import ClassVar, List, Optional
from pydantic import BaseModel, validator, PositiveInt
from pydantic.fields import PrivateAttr
from pydantic.types import constr
from enums import Gender
from dateutil.relativedelta import relativedelta
import itertools

class Player(BaseModel):
    _id_count = itertools.count(1)
    id: PositiveInt = PrivateAttr
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


    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.id = next(Player._id_count)

    


print(Player(first_name='John90àç', last_name='Doe', birthdate='2010-03-30', ranking=2789, gender=Gender.Male))
print(Player(first_name='JORDI', last_name='SHORE', birthdate='2010-03-30', ranking=2789, gender=Gender.Male))
