# content contains data needed in views (text and input types)

from player import Player


player1 = Player(first_name='John', last_name='Doe', birthdate='1989-10-04', ranking=2390, gender='M')
player2 = Player(first_name='Peter', last_name='Callum', birthdate='1970-11-09', ranking=2790, gender='M')
player3 = Player(first_name='Leila', last_name='Erviti', birthdate='1998-03-09', ranking=2890, gender='F')


static_view_content = {
    'MAIN_MENU': {
        'title': 'Welcome to ChessManager 1.0',
        'info': ['Welcome to Chess Manager, your companion to successful chess tournament management.', 'Pick an option from the list below and press enter.'],
        'selectable_options': [{'text': '1. Manage Players', 'route': '/player'}, {'text' : '2. Manage Tournaments', 'route': '/tournament'}, {'text': '3. Generate Data Reports', 'route': '/reports'}, {'text': '4. Manage App Data', 'route': '/appdata'}, {'text': '5. Quit', 'route': '/exit'}],
    },
    'PLAYER_MENU': {
        'title': 'Player Menu',
        'info': ['Create a new player, or edit an existing one.', 'Pick an option from the list below and press enter.', 'Press q and enter to navigate to main menu'],
        'selectable_options': [{'text': '1. Create Player', 'route': '/player/create'}, {'text' : '2. Edit Player', 'route': '/player/edit'}],
      
    },
    'PLAYER_EDIT': {
        'title': 'Edit Players',
        'info': ['Select a player to edit any data from its profile, like ranking.', 'Pick an option from the list below and press enter.', 'Press q and enter to navigate to main menu'],
        'selectable_options':[],
        
    },
    'TOURNAMENT_MENU': {
        'title': 'Tournament Menu',
        'info': ['Create a new tournament, or edit an existing one.','Pick an option from the list below and press enter.', 'Press q and enter to navigate to main menu'],
        'selectable_options': [{'text': '1. Create Tournament', 'route': '/tournament/create'}, {'text' : '2. Edit Tournament', 'route': '/tournament/edit'}],
       
    }
}

app_data = {
    'players': [player1, player2, player3],
    'tournaments': []
}