import os
from typing import List
from view import Form, FormEdit, Menu
from store import static_view_content, app_data

from manager import Router, ViewManager, PlayerManager
from player import Player

def quit_app():
    os.system('cls' if os.name == 'nt' else 'reset')
    exit()

view_manager = ViewManager()
player_manager = PlayerManager()
router = Router(player_manager)


main_menu_content = static_view_content['MAIN_MENU']
edit_player_menu_content = static_view_content['PLAYER_EDIT']
player_menu_content = static_view_content['PLAYER_MENU']
tournament_menu_content = static_view_content['TOURNAMENT_MENU']
player_create_content = static_view_content['PLAYER_CREATE']

main_menu = lambda : Menu(router, *main_menu_content.values())
player_menu = lambda : Menu(router, *player_menu_content.values())
player_create = lambda : Form(router, *player_create_content.values(), player_manager)
tournament_menu = lambda : Menu(router, *tournament_menu_content.values())
player_edit_menu = lambda : Menu(router, *edit_player_menu_content.values(), player_manager.make_option_list())
player_edit_form = lambda : FormEdit(router, *player_create_content.values(), player_manager)

routes = [
    {'path': '/', 'view': main_menu},
    {'path': '/player', 'view': player_menu},
    {'path': '/player/edit', 'view': player_edit_menu},
    {'path': '/tournament', 'view': tournament_menu},
    {'path': '/player/create', 'view': player_create},
    {'path': '/player/edit?', 'view': player_edit_form},
    {'path': '/exit', 'view': quit_app},
]

router(routes)

main_menu().render()