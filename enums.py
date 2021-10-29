from enum import Enum

class Gender(Enum):
    Male = 'M'
    Female = 'F'

class TimeControl(Enum):
    Bullet = 'Bullet'
    Blitz = 'Blitz'
    Rapid = 'Rapid'