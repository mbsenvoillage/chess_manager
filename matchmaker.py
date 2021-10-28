import copy
from os import name
from typing import Dict, List
from player import Player, gen_list_of_players
from tournament import Match, Round, generate_round_results


def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

def generate_first_round_matches(first_half, second_half):
    return list(map(lambda a,b: Match(player_one=a,player_two=b), first_half, second_half))

def generate_round_matches(leaderboard):
    list_of_matches = []
    player_id_list = list(leaderboard)
    for index, player_id in enumerate(player_id_list):
        next_playable_opponent_index = index + 1
        while player_id in leaderboard[player_id_list[next_playable_opponent_index]][2]:
            next_playable_opponent_index += 1
        match = Match(player_one=leaderboard[player_id][0], player_two=leaderboard[player_id_list[next_playable_opponent_index]][0])
        list_of_matches.append(match)
        player_id_list.pop(next_playable_opponent_index)
    return list_of_matches

def generate_matches(rounds, players: List[Player]):
    if len(rounds) == 0:
        players.sort(key=lambda player: player.ranking, reverse=True)
        # [print(player.get_info()) for player in players]
        return generate_first_round_matches(*split_list(players))

def init_leader_board(players: List[Player]):
    leaderboard = {}
    for player in players:
        leaderboard[player.id] = [player, 0, set()]
    return leaderboard

def format_leader_board(leaderboard: Dict):
    str_leaderboard = ''
    for playerId, array in leaderboard.items():
        str_leaderboard += f"{array[0].get_info()} : {array[1]}\n"
    return str_leaderboard

def update_leader_board(leaderboard, round: Round):
    copyOfLeaderboard = copy.deepcopy(leaderboard)
    for match in round.matches:
        copyOfLeaderboard[match.player_one.id][1] += match.player_one_result
        copyOfLeaderboard[match.player_one.id][2].add(match.player_two.id)
        copyOfLeaderboard[match.player_two.id][1] += 1 - match.player_one_result
        copyOfLeaderboard[match.player_two.id][2].add(match.player_one.id)
    return copyOfLeaderboard
    


players = gen_list_of_players(8)
leaderboard = init_leader_board(players)
print(format_leader_board(leaderboard))
leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1][0].ranking, reverse=True))
print(format_leader_board(leaderboard))
matches = generate_matches([], players)
round1 = Round(name='round1',matches=matches)
round1.repr_matches()
r1copy = generate_round_results(round1)
r1copy.repr_matches()
leaderboard = dict(sorted(update_leader_board(leaderboard, r1copy).items(), key=lambda item: item[1][0].ranking, reverse=True))
leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1][1], reverse=True))
print(format_leader_board(leaderboard))
round2_matches = generate_round_matches(leaderboard)
round2 = Round(name='round2', matches=round2_matches)
round2.repr_matches()
r2copy = generate_round_results(round2)
r2copy.repr_matches()
leaderboard = dict(sorted(update_leader_board(leaderboard, r2copy).items(), key=lambda item: item[1][0].ranking, reverse=True))
leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1][1], reverse=True))
print(format_leader_board(leaderboard))