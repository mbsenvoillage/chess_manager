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
        'options': [('1. Create Player', '/player/create'), ('2. Edit Player', '/player/edit')],
    },
    'PLAYER_EDIT': {
        'title': 'Edit Players',
        'info': ['Select a player to edit any data from its profile, like ranking.', 'Pick an option from the list below and press enter.', 'Press q and enter to navigate to main menu'],
    },
    'TOURNAMENT_MENU': {
        'title': 'Tournament Menu',
        'info': ['Create a new tournament, or edit an existing one.','Pick an option from the list below and press enter.', 'Press q and enter to navigate to main menu'],
        'options': [('1. Create Tournament', '/tournament/create'), ('2. Edit Tournament', '/tournament/edit')],
    },
    'PLAYER_CREATE': {
        'title': 'Add New Player',
        'info': ['All form fields must be filled in order to add the new player to the database'],
        'form_fields': [("Player's first name : ", "first_name"), ("Player's last name : ", "last_name"), ("Player's date of birth (yyyy-mm-dd) : ", "birthdate"), ("Player's gender (M/F) : ", "gender"), ("Player's ranking : ", "ranking")]
    }
}

app_data = {
    'players': [player1, player2, player3],
    'tournaments': []
}