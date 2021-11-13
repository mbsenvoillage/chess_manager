import copy
from typing import Dict
from tournament import Match, Round, Tournament


def split_list(a_list) -> set:
    """Splits a list in two halves and returns them in a set"""
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

def generate_first_round_matches(higher_ranking_players, lower_ranking_players):
    return list(map(lambda a,b: Match(player_one=a['id'],player_two=b['id']), higher_ranking_players, lower_ranking_players))

def generate_round_matches(leaderboard):
    list_of_matches = []
    player_id_list = list(leaderboard)
    for index, player_id in enumerate(player_id_list):
        next_playable_opponent_index = index + 1
        try:
            while player_id in leaderboard[player_id_list[next_playable_opponent_index]][2]:
                next_playable_opponent_index += 1
        except IndexError as error:
            print("Cannot generate this round matches followinf the current system")
            print("Some opponents will encounter twice")
            next_playable_opponent_index = index + 1
        match = Match(player_one=player_id, player_two=player_id_list[next_playable_opponent_index])
        list_of_matches.append(match)
        player_id_list.pop(next_playable_opponent_index)
    return list_of_matches

def init_leader_board(players: list[str]) -> dict:
    from manager import PlayerManager
    leaderboard = {}
    for id in players:
        player = PlayerManager().get_by_id(id)
        leaderboard[player['id']] = [player['ranking'], 0, set()]
    return leaderboard



def no_rounds_played(tournament: Tournament) -> bool:
    return len(tournament.rounds) == 0

def all_rounds_played(tournament: Tournament) -> bool:
    return len(tournament.rounds) == tournament.number_of_rounds

def all_round_matches_played(tournament: Tournament) -> bool:
    for match in tournament.rounds[-1].matches:
            if match.player_one_result is None:
                return False
    return True

def update_leaderboard_player_rankings(players: list[dict], leaderboard: dict) -> dict:
    leaderboard = copy.deepcopy(leaderboard)
    for player in players:
        leaderboard[player['id']][0] = player['ranking']
    return leaderboard

def update_leaderboard_standings(leaderboard, round: Round) -> dict:
    leaderboard = copy.deepcopy(leaderboard)
    for match in round.matches:
            leaderboard[match.player_one][1] += match.player_one_result
            leaderboard[match.player_one][2].add(match.player_two)
            leaderboard[match.player_two][1] += 1 - match.player_one_result
            leaderboard[match.player_two][2].add(match.player_one)
    return leaderboard

def sort_leaderboard(leaderboard: dict) -> dict:
    sorted_leaderboard = copy.deepcopy(leaderboard)
    sorted_leaderboard = dict(sorted(sorted_leaderboard.items(), key=lambda item: item[1][0], reverse=True))
    sorted_leaderboard = dict(sorted(sorted_leaderboard.items(), key=lambda item: item[1][1], reverse=True))
    return sorted_leaderboard

def update_leaderboard(players: list[dict],tournament: Tournament) -> dict:
    updated_leaderboard = update_leaderboard_player_rankings(players,tournament.leaderboard)
    updated_leaderboard = update_leaderboard_standings(updated_leaderboard, tournament.rounds[-1])
    updated_leaderboard = sort_leaderboard(updated_leaderboard)
    return updated_leaderboard

def make_round(tournament: Tournament) -> Round:
    from manager import PlayerManager
    tournament = copy.deepcopy(tournament)
    players = [PlayerManager().get_by_id(id) for id in tournament.players]
    if no_rounds_played(tournament):
        players.sort(key=lambda player: player['ranking'], reverse=True)
        round1 = Round(name='Round1', matches=generate_first_round_matches(*split_list(players)))
        return round1
    else:
        if all_rounds_played(tournament):
            raise ValueError('Tournament has reached maximum number of rounds') 
        if not all_round_matches_played(tournament):
            raise ValueError('Cannot generate next round matches until all matches from current round have been played') 
        try:
            new_round = Round(name=f"Round{len(tournament.rounds)}", matches=generate_round_matches(tournament.leaderboard))
        except Exception as e:
            print("Tournament cannot go on with the current matching system")
            raise e
        return new_round


def format_leader_board(leaderboard: Dict):
    from manager import PlayerManager
    str_leaderboard = ''
    for playerId, array in leaderboard.items():
        str_leaderboard += f"{PlayerManager().get_by_id(playerId)['last_name']} : {array[1]}\n"
    return str_leaderboard
            

# players = ['cb803b0f-cffe-45ce-b01f-f49933bfa9bd','b76fbbe8-cfa1-4ba6-bad3-f24c4b872a3d','96fed092-d3bd-4da9-a69d-9ba510cd8447','c8563b04-9d21-4ae1-997e-f2f273a8afbf']
# tournament = Tournament(id=str(uuid.uuid4()),name="artic",venue="norway",number_of_rounds=4,rounds=[],players=players,time_control='Bullet',leaderboard=init_leader_board(players))
# players = [PlayerManager().get_by_id(id) for id in tournament.players]
# round1 = make_round(tournament)
# tournament.rounds.append(round1)
# for index in range(3):
#     tournament.rounds[-1] = generate_round_results(tournament.rounds[-1])
#     for match in tournament.rounds[-1].matches:
#         print(f"{PlayerManager().get_by_id(match.player_one)['last_name']} {match.player_one_result} vs {PlayerManager().get_by_id(match.player_two)['last_name']}") 
#     updated_leaderboard = update_leaderboard(players,tournament)
#     tournament.leaderboard = updated_leaderboard
#     print(format_leader_board(tournament.leaderboard))
#     round = make_round(tournament)
#     tournament.rounds.append(round)

# tournament.rounds[-1] = generate_round_results(tournament.rounds[-1])
# for match in tournament.rounds[-1].matches:
#     print(f"{PlayerManager().get_by_id(match.player_one)['last_name']} {match.player_one_result} vs {PlayerManager().get_by_id(match.player_two)['last_name']}")
# print(format_leader_board(tournament.leaderboard))