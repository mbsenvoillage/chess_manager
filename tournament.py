import random
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import copy
from enums import TimeControl
from player import Player

class Match(BaseModel):
    player_one: str
    player_two: str
    player_one_result: Optional[int]

class Round(BaseModel):
    name: str
    start_time: Optional[date]
    end_time: Optional[date]
    matches: List[Match]

    def repr_matches(self):
        for match in self.matches:
            print(f"{match.player_one.get_info()} vs {match.player_two.get_info()} : {'TBP' if match.player_one_result is None else match.player_one_result} - {'TBP' if match.player_one_result is None else 1 - match.player_one_result}")
        
def generate_round_results(round: Round):
    copyOfRound = copy.deepcopy(round)
    for match in copyOfRound.matches:
        match.player_one_result =[0,0.5,1][random.randint(0,2)]
    return copyOfRound

class Tournament(BaseModel):
    id: str 
    name: str
    venue: str
    start_date: Optional[date]
    end_date: Optional[date]
    number_of_rounds: int = 4
    rounds: list[Round]
    players: list[str]
    time_control: TimeControl
    comments: str = ''
    leaderboard: dict = {}

    def __init__(__pydantic_self__, **data: any) -> None:
        super().__init__(**data)
        if len(__pydantic_self__.rounds) == 0:
            __pydantic_self__.init_leader_board()
            __pydantic_self__.players.sort(key=lambda player: player.ranking, reverse=True)
            round1 = Round(name='Round1', matches=__pydantic_self__.generate_first_round_matches(*__pydantic_self__.split_list(__pydantic_self__.players)))
            __pydantic_self__.rounds.append(round1)
        else:
            print("will not init leaderboard")

    def init_leader_board(self) -> dict:
        leaderboard = {}
        for player_id in self.players:
            leaderboard[player_id] = [player_id, 0, set()]
        self.leaderboard = leaderboard
        return leaderboard

    def update_leader_board(self) -> dict:
        self.update_leaderboard_player_rankings()
        for match in self.rounds[-1].matches:
            self.leaderboard[match.player_one.id][1] += match.player_one_result
            self.leaderboard[match.player_one.id][2].add(match.player_two.id)
            self.leaderboard[match.player_two.id][1] += 1 - match.player_one_result
            self.leaderboard[match.player_two.id][2].add(match.player_one.id)
        self.sort_leaderboard()
        return self.leaderboard
    
    def update_leaderboard_player_rankings(self) -> dict:
        for player in self.players:
            self.leaderboard[player.id][0] = player
        return self.leaderboard

    def sort_leaderboard(self):
        self.leaderboard = dict(sorted(self.leaderboard.items(), key=lambda item: item[1][0].ranking, reverse=True))
        self.leaderboard = dict(sorted(self.leaderboard.items(), key=lambda item: item[1][1], reverse=True))
        return self.leaderboard

    def make_round(self):
        if len(self.rounds) == self.number_of_rounds:
            raise ValueError('Tournament has reached maximum number of rounds') 
        for match in self.rounds[-1].matches:
            if match.player_one_result is None:
                raise ValueError('Cannot generate next round matches until all matches from current round have been played') 
        self.update_leader_board()
        try:
            new_round = Round(name=f"Round{len(self.rounds)}", matches=self.generate_round_matches(self.leaderboard))
        except Exception as e:
            print(e)
            print("Tournament cannot go on with the current matching system")
            raise e
        self.rounds.append(new_round)
        return self

    def generate_round_matches(self):
        list_of_matches = []
        player_id_list = list(self.leaderboard)
        for index, player_id in enumerate(player_id_list):
            next_playable_opponent_index = index + 1
            try:
                while player_id in self.leaderboard[player_id_list[next_playable_opponent_index]][2]:
                    next_playable_opponent_index += 1
            except IndexError as error:
                print("Cannot generate this round matches")
                raise error
            #Now storing player IDs in match
            match = Match(player_one=player_id, player_two=player_id_list[next_playable_opponent_index])
            list_of_matches.append(match)
            player_id_list.pop(next_playable_opponent_index)
        return list_of_matches

    def split_list(self,a_list):
        half = len(a_list)//2
        return a_list[:half], a_list[half:]

    def generate_first_round_matches(self,first_half, second_half):
        return list(map(lambda a,b: Match(player_one=a,player_two=b), first_half, second_half))
 
    @validator('players')
    def is_number_of_players_even(cls, value):
        if len(value) % 2 != 0:
            raise ValueError('Number of participants should be even')
        return value
 
    @validator('players')
    def is_number_of_players_sufficient(cls, value):
        if len(value) < 8:
            raise ValueError('There should be at least eight participants for the tournament')
        return value
