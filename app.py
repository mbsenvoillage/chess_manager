import os
from View.view import Form, FormField, Menu
from View.content_loader import ViewContentLoader
from View.option_builder import ViewSelectableOptionBuilder

import manager
from player import Player

def quit_app():
    os.system('cls' if os.name == 'nt' else 'reset')
    exit()

view_manager = manager.ViewManager()
content_loader = ViewContentLoader()
player_manager = manager.PlayerManager()
main_menu = Menu(view_manager, content_loader, 'MAIN_MENU')
player_menu = Menu(view_manager, content_loader, 'PLAYER_MENU')
player_create = Form(view_manager, content_loader, 'PLAYER_CREATE', player_manager)

edit_player_menu_selectable_options_builder = ViewSelectableOptionBuilder('{_id}. {first_name} {last_name}', 'players', '/player/edit/someone')
edit_player_menu = Menu(view_manager, content_loader.plug_selectable_option_builder(edit_player_menu_selectable_options_builder), 'PLAYER_EDIT')
tournament_menu = Menu(view_manager, content_loader, 'TOURNAMENT_MENU')
view_manager.add_route('/', main_menu)
view_manager.add_route('/player', player_menu)
view_manager.add_route('/player/edit', edit_player_menu)
view_manager.add_route('/tournament', tournament_menu)
view_manager.add_route('/player/create', player_create)
view_manager.add_route('/exit', quit_app)


main_menu.render()