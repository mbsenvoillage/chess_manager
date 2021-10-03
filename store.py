# content contains data needed in views (text and input types)

from player import Player


player1 = Player(first_name='John', last_name='Doe', birthdate='1989-10-04', ranking=2390, gender='M')
player2 = Player(first_name='Peter', last_name='Callum', birthdate='1970-11-09', ranking=2790, gender='M')
player3 = Player(first_name='Leila', last_name='Erviti', birthdate='1998-03-09', ranking=2890, gender='F')


view_data = {
    'MAIN_MENU': {
        'title': 'Welcome to ChessManager 1.0',
        'info': ['Welcome to Chess Manager, your companion to successful chess tournament management.', 'Pick an option from the list below and press enter.'],
        'main': [{'text': '1. Manage Players', 'route': '/playermenu'}, {'text' : '2. Manage Tournaments', 'route': '/tournamentmenu'}, {'text': '3. Generate Data Reports', 'route': '/reportsmenu'}, {'text': '4. Manage App Data', 'route': '/appdatamenu'}, {'text': '5. Quit', 'route': '/exit'}],
        'prompt': '>>> '
    }
}

app_data = {
    'players': [player1, player2, player3],
    'tournaments': []
}