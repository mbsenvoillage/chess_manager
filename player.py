from datetime import date
from pydantic import BaseModel, validator, PositiveInt
from pydantic.fields import PrivateAttr
from pydantic.types import constr
from enums import Gender
from dateutil.relativedelta import relativedelta

    # [TODO] first name must not contain more than 25 letters and less than 2
    # may contain spaces, accents, dashes
    # may not contain numbers, special charactersc
class Player(BaseModel):
    id: str
    first_name: constr(strip_whitespace=True, min_length=2, max_length=25)
    last_name: constr(strip_whitespace=True, min_length=2, max_length=25)
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

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

