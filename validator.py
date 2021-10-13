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