# content contains data needed in views (text and input types)

from player import Player


player1 = Player(first_name='John', last_name='Doe', birthdate='1989-10-04', ranking=2390, gender='M')
player2 = Player(first_name='Peter', last_name='Callum', birthdate='1970-11-09', ranking=2790, gender='M')
player3 = Player(first_name='Leila', last_name='Erviti', birthdate='1998-03-09', ranking=2890, gender='F')

static_view_content = {
    'MAIN_MENU': {
        'title': 'Welcome to ChessManager 1.0',
        'info': ['Welcome to Chess Manager, your companion to successful chess tournament management.', 'Pick an option from the list below and press enter.'],
        'options': [('1. Manage Players', '/player'), ('2. Manage Tournaments','/tournament'), ('3. Generate Data Reports', '/reports'), ('4. Manage App Data', '/appdata'), ('5. Quit','/exit')],
    },
    'PLAYER_MENU': {
        'title': 'Player Menu',
        'info': ['Create a new player, or edit an existing one.', 'Pick an option from the list below and press enter.', 'Press q and enter to navigate to main menu'],
        'options': [{'text': '1. Create Player', 'route': '/player/create'}, {'text' : '2. Edit Player', 'route': '/player/edit'}],
    },
    'PLAYER_EDIT': {
        'title': 'Edit Players',
        'info': ['Select a player to edit any data from its profile, like ranking.', 'Pick an option from the list below and press enter.', 'Press q and enter to navigate to main menu'],
        'options':[],
    },
    'TOURNAMENT_MENU': {
        'title': 'Tournament Menu',
        'info': ['Create a new tournament, or edit an existing one.','Pick an option from the list below and press enter.', 'Press q and enter to navigate to main menu'],
        'options': [{'text': '1. Create Tournament', 'route': '/tournament/create'}, {'text' : '2. Edit Tournament', 'route': '/tournament/edit'}],
    },
    'PLAYER_CREATE': {
        'title': 'Add New Player',
        'info': ['All form fields must be filled in order to add the new player to the database'],
        'form_fields': [{"text": "Player's first name : ", "class_attribute": "first_name"}, {"text": "Player's last name : ", "class_attribute": "last_name"}, {"text":"Player's date of birth (yyyy-mm-dd) : ", "class_attribute": "birthdate"}, {"text": "Player's gender (M/F) : ", "class_attribute": "gender"}, {"text": "Player's ranking : ", "class_attribute": "ranking"}]
    }
}

app_data = {
    'players': [player1, player2, player3],
    'tournaments': []
}