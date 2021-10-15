import os
from typing import List
from View.view import Form, Menu
from store import static_view_content, app_data

import manager
from player import Player

def quit_app():
    os.system('cls' if os.name == 'nt' else 'reset')
    exit()

main_menu_content = static_view_content['MAIN_MENU']
edit_player_menu_content = static_view_content['PLAYER_EDIT']
player_option_list: List[Player] = [player.make_view_option('/player/edit') for player in app_data['players']]
player_menu_content = static_view_content['PLAYER_MENU']
tournament_menu_content = static_view_content['TOURNAMENT_MENU']
player_create_content = static_view_content['PLAYER_CREATE']

view_manager = manager.ViewManager()
player_manager = manager.PlayerManager()

main_menu = Menu(view_manager, *main_menu_content.values())
edit_player_menu = Menu(view_manager, *edit_player_menu_content.values(), player_option_list)
player_menu = Menu(view_manager, *player_menu_content.values())
player_create = Form(view_manager, *player_create_content.values(), player_manager)

tournament_menu = Menu(view_manager, *tournament_menu_content.values())


view_manager.add_route('/', main_menu)
view_manager.add_route('/player', player_menu)
view_manager.add_route('/player/edit', edit_player_menu)
view_manager.add_route('/tournament', tournament_menu)
view_manager.add_route('/player/create', player_create)
view_manager.add_route('/exit', quit_app)

main_menu.render()