import random
from tinydb import TinyDB, Query, table, where

from tournament import Tournament

db = TinyDB('db.json')

players = db.table('players')
tournaments = db.table('tournaments')

tournament = tournaments.search(where('id') == '3ec55c80-a737-42f9-b061-754dbf7a0d0b')[0]

# for match in tournament['rounds'][-1]['matches']:
#     match['player_one_result'] = [0,0.5,1][random.randint(0,2)]

# tournaments.update(tournament, where('id') == '3ec55c80-a737-42f9-b061-754dbf7a0d0b')

def set_matches(path, val):
    def transform(doc):
        for idx, match in enumerate(doc[path][-1]['matches']):
            match['player_one_result'] = val[idx]
    return transform


# tournaments.update(set_matches('rounds', [0,1,1,1]), where('id') == '3ec55c80-a737-42f9-b061-754dbf7a0d0b')
# for tournament in tournaments.all():
#     new_tournament = Tournament(**tournament)
#     print(new_tournament)

