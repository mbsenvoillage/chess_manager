from datetime import date, datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta
from Model.player import Player

def validate_player_firstname(name: str) -> bool:
    import re
    name = name.strip()
    if len(name) < 3 or len(name) > 25:
        return False
    regex = re.compile("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$")
    return regex.match(name)

def validate_player_lastname(name: str) -> bool:
    import re
    name = name.strip()         
    if len(name) < 3 or len(name) > 25:
        return False
    regex = re.compile("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$")
    return regex.match(name)


def validate_player_birthdate(birthdate: str) -> bool:
    # players must be at least 6
    try:
        isValid = parser.parse(birthdate) < (datetime.today() - relativedelta(years=6))
        return isValid
    except Exception as e:
        return False

def validate_player_ranking(ranking: str) -> bool:
    # min=300 #max=3000
    try:
        isValid = int(ranking) > 300 and int(ranking) < 3000
        return isValid
    except Exception as e:
        return False


def validate_player_gender(gender: str) -> bool:
    # m/f case insensitive
    try:
        isValid = gender.lower() in ['m', 'f']
        return isValid
    except Exception as e:
        return False


player_validators = {
    'first_name': validate_player_firstname,
    'last_name': validate_player_lastname,
    'birthdate': validate_player_birthdate,
    'ranking': validate_player_ranking,
    'gender': validate_player_gender
}


def validate_tournament_name(name: str) -> bool:
    import re
    name = name.strip()
    if len(name) < 2 or len(name) > 25:
        return False
    regex = re.compile("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$")
    return regex.match(name) and len(name) > 2 and len(name) < 100

def validate_tournament_venue(name: str) -> bool:
    import re
    name = name.strip()
    if len(name) < 2 or len(name) > 25:
        return False
    regex = re.compile("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$")
    return regex.match(name) and len(name) > 2 and len(name) < 100


def validate_tournament_start_date(start_date: str) -> bool:
    isValid: bool
    if len(start_date) is not 10:
        isValid = False
    else:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        try:
            isValid = parser.parse(f'{start_date} {current_time}') >= (datetime.now() - relativedelta(hours=1))
        except Exception as e:
            isValid = False
    return isValid


def validate_tournament_end_date(end_date: str) -> bool:
    isValid: bool
    if len(end_date) is not 10:
        isValid = False
    else:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        try:
            isValid = parser.parse(f'{end_date} {current_time}') >= (datetime.now() - relativedelta(hours=1))
        except Exception as e:
            isValid = False
    return isValid

def validate_tournament_number_of_rounds(number_of_rounds: str) -> bool:
    isValid: bool
    try:
        # field can be left empty since default value is 4
        if not number_of_rounds:
            isValid = True
        else:
            isValid = int(number_of_rounds) >= 4
    except Exception as e:
        isValid = False
    return isValid


def validate_tournament_players(players: str) -> bool:
    from DAL.manager import PlayerManager
    isValid: bool
    valid_players = [repr(player) for player in PlayerManager().get_all()]
    try:
        list_of_players = list(filter(bool, players.split(' / ')))
        # list shouldn't contain duplicates
        if len(list_of_players) != len(set(list_of_players)):
            isValid = False
        else:
            # submitted players should be valid
            for player in list_of_players:
                valid_player = player + ' / '
                if valid_player not in valid_players:
                    return False
            isValid = len(list_of_players) >= 8
    except Exception as e:
        isValid = False
    return isValid

def validate_tournament_time_control(time_control: str) -> bool:
    try:
        isValid = time_control.lower() in ['blitz', 'rapid', 'bullet']
        return isValid
    except Exception as e:
        return False


def validate_tournament_comments(comments: str) -> bool:
    return len(comments) < 2000


def validate_tournament_match(score: str) -> bool:
    return score in ['0', '0.5', '1']


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