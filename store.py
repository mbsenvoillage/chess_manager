# content contains data needed in views (text and input types)

view_data = {
    'MAIN_MENU': {
        'title': 'Welcome to ChessManager 1.0',
        'info': ['Welcome to Chess Manager, your companion to successful chess tournament management.', 'Pick an option from the list below and press enter.'],
        'main': {1: {'text': '1. Manage Players', 'route': '/playermenu'}, 2: {'text' : '2. Manage Tournaments', 'route': '/tournamentmenu'}, 3: {'text': '3. Generate Data Reports', 'route': '/reportsmenu'}, 4: {'text': '4. Manage App Data', 'route': '/appdatamenu'}, 5: {'text': '5. Quit', 'route': '/exit'}},
        'prompt': '>>> '
    }
}