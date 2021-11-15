from datetime import date
from player import Player

def validate_player_firstname(name: str) -> bool:
    #trim
    #min_length=2 max_length=25
    return True

def validate_player_lastname(name: str) -> bool:
    #trim
    #min_length=2 max_length=25
    return True

def validate_player_birthdate(birthdate: str) -> bool:
    #players must be at least 6
    return True

def validate_player_ranking(ranking: str) -> bool:
    #min=1 #max=3000
    return True

def validate_player_gender(gender) -> bool:
    #m/f case insensitive
    return True

player_validators = {
        'first_name': validate_player_firstname,
        'last_name': validate_player_lastname,
        'birthdate': validate_player_birthdate,
        'ranking': validate_player_ranking,
        'gender': validate_player_gender
    }

def validate_tournament_name(name: str) -> bool:
    return True

def validate_tournament_venue(name: str) -> bool:
    return True

def validate_tournament_start_date(start_date: date) -> bool:
    return True

def validate_tournament_end_date(end_date: date) -> bool:
    return True

def validate_tournament_number_of_rounds(number_of_rounds: int) -> bool:
    return True

def validate_tournament_players(players: list[Player]) -> bool:
    return True

def validate_tournament_time_control(time_control: str) -> bool:
    return True

def validate_tournament_comments(comments: str) -> bool:
    return True

def validate_tournament_match(score: str) -> bool:
    return score in ['0','0.5','1']

tournament_validators = {
    'name': validate_tournament_name,
    'venue': validate_tournament_venue,
    'start_date': validate_tournament_start_date,
    'end_date': validate_tournament_end_date,
    'number_of_rounds': validate_tournament_number_of_rounds,
    'players': validate_tournament_players,
    'time_control': validate_tournament_time_control,
    'comments': validate_tournament_comments,
    'match': validate_tournament_match,
}