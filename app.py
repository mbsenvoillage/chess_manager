import os
from player import Player
# from view import Completer, Form, FormEdit, Menu, Report
# from store import static_view_content
from manager import PlayerManager
from Router.router import Router
from Controllers.controllers import CreatePlayerFormController, EditPlayerFormController, EditPlayerMenuController, MainMenuContoller, PlayerMenuController

class App():

    __mount_point: callable

    def __init__(self) -> None:
        # tournament_menu_content = static_view_content['TOURNAMENT_MENU']
        # tournament_create_content = static_view_content['TOURNAMENT_CREATE']
        # tournament_edit_content = static_view_content['TOURNAMENT_EDIT_MENU']
        # edit_tournament_menu_content = static_view_content['TOURNAMENT_EDIT_FORM']
        # reports_menu_content = static_view_content['REPORTS_MENU']
        # reports_menu_player_content = static_view_content['REPORTS_MENU_PLAYER']
        # reports_player_alpha = static_view_content['REPORTS_PLAYER_ALPHA']
        # reports_player_ranking = static_view_content['REPORTS_PLAYER_RANKING']

        # player_reports_table_headers =['Last Name', 'First Name', 'Ranking', 'Birthdate']

        # players_for_autocomplete = lambda : [repr(player) for player in player_manager.get_all()]
        # get_editable_tournaments = lambda: tournament_manager.make_option_list('/tournament/edit/form?id=')
        # get_players_sorted_alphabetically = lambda: [[player.last_name,player.first_name,player.ranking,player.birthdate] for player in player_manager.get_all(order_by='alpha')]
        # get_players_sorted_by_ranking = lambda: [[player.last_name,player.first_name,player.ranking,player.birthdate] for player in player_manager.get_all(order_by='ranking')]

        # player_edit_form = lambda : FormEdit('player_edit_form',router, *edit_player_form_content.values(), view_manager)
        # tournament_menu = lambda : Menu('tournament',router, *tournament_menu_content.values())
        # tournament_create = lambda : Form('tournament_create',router,*tournament_create_content.values(), view_manager, Completer(players_for_autocomplete(),'players'))
        # tournament_edit_menu = lambda : Menu('tournament_edit_menu',router,*tournament_edit_content.values(),get_editable_tournaments())
        # tournament_edit_form  = lambda : Form('tournament_edit_form',router,*edit_tournament_menu_content.values(),form_fields=[],view_manager=view_manager)
        # reports_menu = lambda : Menu('reports',router,*reports_menu_content.values())
        # reports_menu_player = lambda : Menu('reports_player',router,*reports_menu_player_content.values())
        # reports_players_sorted_alphabetically = lambda: Report('reports_player_alpha',router,*reports_player_alpha.values(), get_players_sorted_alphabetically(),player_reports_table_headers)
        # reports_players_sorted_by_ranking = lambda: Report('reports_player_ranking',router,*reports_player_ranking.values(), get_players_sorted_by_ranking(),player_reports_table_headers)


        # views = {'': {'view': main_menu, 'manager': None}, 
        # 'player': {'view': player_menu, 'manager': None}, 
        # 'player_create': {'view': player_create, 'manager': player_manager},
        # 'player_edit_menu': {'view': player_edit_menu, 'manager': None},
        # 'player_edit_form': {'view': player_edit_form, 'manager': player_manager},
        # 'tournament': {'view': tournament_menu, 'manager': None},
        # 'tournament_create': {'view': tournament_create, 'manager': tournament_manager},
        # 'tournament_edit_menu': {'view': tournament_edit_menu, 'manager': None},
        # 'tournament_edit_form': {'view': tournament_edit_form, 'manager': tournament_manager},
        # 'reports': {'view': reports_menu,'manager': None},
        # 'reports_player': {'view': reports_menu_player, 'manager': None},
        # 'reports_player_alpha': {'view': reports_players_sorted_alphabetically, 'manager': None},
        # 'reports_player_ranking': {'view': reports_players_sorted_by_ranking, 'manager': None},
        # 'exit': {'view': self.__quit_app, 'manager': None}
        # }
        # router = Router(view_manager(views))
        router = Router()
        player_manager = PlayerManager()

        main_menu_controller = MainMenuContoller(router)
        player_menu_controller = PlayerMenuController(router)
        player_create_controller = CreatePlayerFormController(router,player_manager)
        player_edit_menu_controller = EditPlayerMenuController(router,player_manager)
        player_edit_form_controller = EditPlayerFormController(router,player_manager)

        router.add_route('/',main_menu_controller)
        router.add_route('/player',player_menu_controller)
        router.add_route('/player/create',player_create_controller)
        router.add_route('/player/edit/menu',player_edit_menu_controller)
        router.add_route('/player/edit/form?', player_edit_form_controller)


        self.__mount_point = router.start

    def __quit_app(self):
        os.system('cls' if os.name == 'nt' else 'reset')
        exit()

    def run(self):
        self.__mount_point()
