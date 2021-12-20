import copy
from datetime import datetime
from typing import Dict
from Model.tournament import Match, Round, Tournament


def split_list(a_list) -> set:
    """Splits a list in two halves and returns them in a set"""
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]


def generate_first_round_matches(higher_ranking_players, lower_ranking_players):
    return list(map(lambda a,
                    b: Match(player_one=a['id'],
                             player_two=b['id']),
                    higher_ranking_players,
                    lower_ranking_players))


def generate_round_matches(leaderboard):
    list_of_matches = []
    player_id_list = list(leaderboard)
    for index, player_id in enumerate(player_id_list):
        next_playable_opponent_index = index + 1
        try:
            while player_id in leaderboard[player_id_list[next_playable_opponent_index]][2]:
                next_playable_opponent_index += 1
        except IndexError as error:
            print(error)
            print("Cannot generate this round matches following the current system")
            print("Some opponents will encounter twice")
            next_playable_opponent_index = index + 1
        match = Match(player_one=player_id, player_two=player_id_list[next_playable_opponent_index])
        list_of_matches.append(match)
        player_id_list.pop(next_playable_opponent_index)
    return list_of_matches


def init_leader_board(players: list[str]) -> dict:
    from DAL.manager import PlayerManager
    leaderboard = {}
    for id in players:
        player = PlayerManager().get_by_id(id)
        leaderboard[player['id']] = [player['ranking'], 0, []]
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
        leaderboard[match.player_one][1] += int(match.player_one_result)
        leaderboard[match.player_one][2].append(match.player_two)
        leaderboard[match.player_two][1] += 1 - int(match.player_one_result)
        leaderboard[match.player_two][2].append(match.player_one)
    return leaderboard


def sort_leaderboard(leaderboard: dict) -> dict:
    sorted_leaderboard = copy.deepcopy(leaderboard)
    sorted_leaderboard = dict(sorted(sorted_leaderboard.items(), key=lambda item: item[1][0], reverse=True))
    sorted_leaderboard = dict(sorted(sorted_leaderboard.items(), key=lambda item: item[1][1], reverse=True))
    return sorted_leaderboard


def update_leaderboard(players: list[dict], tournament: Tournament) -> dict:
    updated_leaderboard = update_leaderboard_player_rankings(players, tournament.leaderboard)
    updated_leaderboard = update_leaderboard_standings(updated_leaderboard, tournament.rounds[-1])
    updated_leaderboard = sort_leaderboard(updated_leaderboard)
    return updated_leaderboard


def make_round(tournament: Tournament) -> Round:
    from DAL.manager import PlayerManager
    tournament = copy.deepcopy(tournament)
    players = [PlayerManager().get_by_id(id) for id in tournament.players]
    if no_rounds_played(tournament):
        players.sort(key=lambda player: player['ranking'], reverse=True)
        round1 = Round(name='Round1', matches=generate_first_round_matches(*split_list(players)), start_time=datetime.now())
        return round1
    else:
        if all_rounds_played(tournament):
            raise ValueError('Tournament has reached maximum number of rounds')
        if not all_round_matches_played(tournament):
            raise ValueError('Cannot generate next round matches until all matches from current round have been played')
        try:
            new_round = Round(
                name=f"Round{len(tournament.rounds)+1}",
                matches=generate_round_matches(
                    tournament.leaderboard),
                    start_time=datetime.now())
        except Exception as e:
            print("Tournament cannot go on with the current matching system")
            raise e
        return new_round


def format_leader_board(leaderboard: Dict):
    from DAL.manager import PlayerManager
    str_leaderboard = ''
    for playerId, array in leaderboard.items():
        str_leaderboard += f"{PlayerManager().get_by_id(playerId)['last_name']} : {array[1]}\n"
    return str_leaderboard
