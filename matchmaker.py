import copy
from os import error, name
from typing import Dict, List
from player import Player, gen_list_of_players
from tournament import Match, Round, Tournament, generate_round_results

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
        try:
            while player_id in leaderboard[player_id_list[next_playable_opponent_index]][2]:
                next_playable_opponent_index += 1
        except IndexError as error:
            print("Cannot generate this round matches")
            raise error
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

def make_round(tournament: Tournament):
    if len(tournament.rounds) == 0:
        tournament.players.sort(key=lambda player: player.ranking, reverse=True)
        round1 = Round(name='Round1', matches=generate_first_round_matches(*split_list(tournament.players)))
        tournament.rounds.append(round1)
        return tournament
    else:
        if len(tournament.rounds) == tournament.number_of_rounds:
            raise ValueError('Tournament has reached maximum number of rounds') 
        for match in tournament.rounds[len(tournament.rounds)-1].matches:
            if match.player_one_result is None:
                raise ValueError('Cannot generate next round matches until all matches from current round have been played') 
        leaderboard = init_leader_board(tournament.players)
        for round in tournament.rounds:
            leaderboard = dict(sorted(update_leader_board(leaderboard, round).items(), key=lambda item: item[1][0].ranking, reverse=True))
            leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1][1], reverse=True))
        try:
            new_round = Round(name=f"Round{len(tournament.rounds)}", matches=generate_round_matches(leaderboard))
        except Exception as e:
            print(e)
            print("Tournament cannot go on with the current matching system")
            raise e
        tournament.rounds.append(new_round)
        return tournament
            
tournament = Tournament(name="Arctic Chess",venue="Royal Palace of Norway",rounds=[],players=gen_list_of_players(8),time_control='Bullet')

leaderboard = init_leader_board(tournament.players)
print(format_leader_board(leaderboard))
leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1][0].ranking, reverse=True))
try:
    for round_idx in range(tournament.number_of_rounds):
        tournament = make_round(tournament)
        tournament.rounds[round_idx] = generate_round_results(tournament.rounds[round_idx])
        tournament.rounds[round_idx].repr_matches()
        leaderboard = dict(sorted(update_leader_board(leaderboard, tournament.rounds[round_idx]).items(), key=lambda item: item[1][0].ranking, reverse=True))
        leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1][1], reverse=True))
        print(format_leader_board(leaderboard))
except Exception as e:
    print("Tournament must end now")
