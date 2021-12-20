from datetime import date
from pydantic import BaseModel, validator, PositiveInt
from pydantic.types import constr
from Model.enums import Gender
from dateutil.relativedelta import relativedelta

class Player(BaseModel):
    id: str
    first_name: constr(strip_whitespace=True, min_length=2, max_length=25)
    last_name: constr(strip_whitespace=True, min_length=2, max_length=25)
    birthdate: date
    ranking: PositiveInt
    gender: Gender


    @validator('ranking')
    def ranking_validator(cls, value):
        if value > 3000:
            raise ValueError('Ranking must not exceed 3000')
        return value

    @validator('birthdate')
    def player_must_be_at_least_six(cls, value):
        if value > (date.today() - relativedelta(years=6)):
            raise ValueError('Player must be at least six years old')
        return value

    @validator('first_name')
    def first_name_validator(cls, value):
        import re
        name = value.strip()
        if len(name) < 3 or len(name) > 25:
            raise ValueError("Player's first name must contain at least two letters and no more than 25")
        regex = re.compile("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$")
        if not regex.match(name):
            raise ValueError("Player's first name cannot contain numbers or special characters")
        return value

    @validator('last_name')
    def last_name_validator(cls, value):
        import re
        name = value.strip()
        if len(name) < 3 or len(name) > 25:
            raise ValueError("Player's last name must contain at least two letters and no more than 25")
        regex = re.compile("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$")
        if not regex.match(name):
            raise ValueError("Player's last name cannot contain numbers or special characters")
        return value

    def __init__(self, **data) -> None:
        super().__init__(**data)

    def __repr__(self):
        return f"{self.last_name} {self.first_name} {self.birthdate} {self.ranking} / "

    def get_info(self):
        return f"{self.last_name}, {self.first_name} - Ranking : {self.ranking} - Birthdate : {self.birthdate}"