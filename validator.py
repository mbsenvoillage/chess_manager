def validate_player_name(name: str) -> bool:
    #trim
    #min_length=2 max_length=25
    print('hello')

def validate_player_birthdate(birthdate: str) -> bool:
    #players must be at least 6
    pass

def validate_player_ranking(ranking: str) -> bool:
    #min=1 #max=3000
    pass

def validate_player_gender() -> bool:
    #m/f case insensitive
    pass

player_validators = {
        'name': validate_player_name,
        'birthdate': validate_player_birthdate,
        'ranking': validate_player_ranking,
        'gender': validate_player_gender
    }