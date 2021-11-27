from datetime import date
from pydantic import BaseModel, validator, PositiveInt
from pydantic.types import constr
from enums import Gender
from dateutil.relativedelta import relativedelta
import names
import random
import uuid

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
        return f"{self.last_name} {self.first_name} {self.birthdate} {self.ranking} / "
    
    def get_info(self):
        return f"{self.last_name}, {self.first_name} - Ranking : {self.ranking} - Birthdate : {self.birthdate}"


def gen_birthdate():
    return f"{random.randint(1940,1990)}-{random.randint(1,12)}-{random.randint(1,28)}"

def gen_gender():
    return ['M', 'F'][random.randint(0,1)]

def gen_id():
    return str(uuid.uuid4())

def gen_ranking():
    return random.randint(1000,3000)

def gen_player():
    return Player(id=gen_id(), first_name=names.get_first_name(), last_name=names.get_last_name(), birthdate=gen_birthdate(), ranking=gen_ranking(), gender=gen_gender())

def gen_list_of_players(number):
    return [gen_player() for i in range(int(number))]




# players = gen_list_of_players(8)
# players.sort(key=lambda player: player.ranking, reverse=True)

# for player in players:
#     print(player.get_info())‡