from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, validator, PositiveInt
from enums import Gender






class Player(BaseModel):
    id: PositiveInt
    first_name: str
    last_name: str
    birthdate: date
    ranking: PositiveInt
    gender: Gender

    # @validator('id')
    # def id_must_be_positive(cls, value):
    #     if value < 0:
    #         raise ValueError('id must be positive integers')
    #     return value

    
 

print(Player(id=2, first_name='John', last_name='Doe', birthdate='1989-03-30', ranking=2789, gender=Gender.Male))