class Leaderboard(object):

    board: dict = {}
    players: list[dict]

    def __init__(self,players) -> None:
        self.players = players
        self.init_leader_board()

    def init_leader_board(self) -> None:
        leaderboard = {}
        for player in self.players:
            leaderboard[player['id']] = [player['ranking'],0, set()]
        leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1][0], reverse=True))
        self.board = leaderboard



leaderboard = Leaderboard(players=[{'id': 'cb803b0f-cffe-45ce-b01f-f49933bfa9bd', 'ranking': 2987},
{'id': 'b76fbbe8-cfa1-4ba6-bad3-f24c4b872a3d', 'ranking': 2675},
{'id': '96fed092-d3bd-4da9-a69d-9ba510cd8447', 'ranking': 2780},
{'id': 'c8563b04-9d21-4ae1-997e-f2f273a8afbf', 'ranking': 2456}])

print(leaderboard.board)
print(list(leaderboard.board.keys()))