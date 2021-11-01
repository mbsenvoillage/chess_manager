import os
from view import Form, FormEdit, Menu
from store import static_view_content
from manager import Router, ViewManager, PlayerManager

class App():

    __mount_point: callable

    def __init__(self) -> None:
        player_manager = PlayerManager()
        view_manager = ViewManager()

        main_menu_content = static_view_content['MAIN_MENU']
        edit_player_menu_content = static_view_content['PLAYER_EDIT']
        player_menu_content = static_view_content['PLAYER_MENU']
        tournament_menu_content = static_view_content['TOURNAMENT_MENU']
        player_create_content = static_view_content['PLAYER_CREATE']
        get_editable_players = lambda: player_manager.make_option_list('/player/edit/form?id=')

        main_menu = lambda : Menu('main',router, *main_menu_content.values())
        player_menu = lambda : Menu('player',router, *player_menu_content.values())
        player_create = lambda : Form('player_create',router, *player_create_content.values(), view_manager)
        tournament_menu = lambda : Menu('tournament',router, *tournament_menu_content.values())
        player_edit_menu = lambda : Menu('player_edit_menu',router, *edit_player_menu_content.values(), get_editable_players())
        player_edit_form = lambda : FormEdit('player_edit_form',router, *player_create_content.values(), view_manager)

        views = {'': {'view': main_menu, 'manager': None}, 
        'player': {'view': player_menu, 'manager': None}, 
        'player_create': {'view': player_create, 'manager': player_manager},
        'player_edit_menu': {'view': player_edit_menu, 'manager': None},
        'player_edit_form': {'view': player_edit_form, 'manager': player_manager},
        'tournament': {'view': tournament_menu, 'manager': None},
        'exit': {'view': self.__quit_app, 'manager': None}
        }
        router = Router(view_manager(views))
        self.__mount_point = main_menu().render

    def __quit_app(self):
        os.system('cls' if os.name == 'nt' else 'reset')
        exit()

    def run(self):
        self.__mount_point()



