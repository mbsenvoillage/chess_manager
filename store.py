# content contains data needed in views (text and input types)

view_data = {
    'MAIN_MENU': {
        'title': 'Welcome to ChessManager 1.0',
        'info': ['Welcome to Chess Manager, your companion to successful chess tournament management.', 'Pick an option from the list below and press enter.'],
        'main': [{'text': '1. Manage Players', 'route': '/playermenu'}, {'text' : '2. Manage Tournaments', 'route': '/tournamentmenu'}, {'text': '3. Generate Data Reports', 'route': '/reportsmenu'}, {'text': '4. Manage App Data', 'route': '/appdatamenu'}, {'text': '5. Quit', 'route': '/exit'}],
        'prompt': '>>> '
    }
}

app_data = {
    'players': [],
    'tournaments': []
}