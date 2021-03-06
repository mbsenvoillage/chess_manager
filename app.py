from DAL.manager import PlayerManager, TournamentManager
from Router.router import Router
from Controllers.controllers import (CreatePlayerFormController, CreateTournamentFormController,
                                     EditPlayerFormController, EditPlayerMenuController,
                                     EditTournamentFormController, EditTournamentMenuController, ErrorPageContoller,
                                     ExitController, MainMenuContoller, NotEnoughPlayersErrorPageContoller, PlayerMenuController,
                                     PlayerReportsController, ReportsMenuController, TournamentMenuController,
                                     TournamentReportsController, TournamentReportsMenuController)


class App():

    launch: callable
    salvage_app: callable

    def __init__(self) -> None:
        router = Router()
        player_manager = PlayerManager()
        tournament_manager = TournamentManager(player_manager)

        main_menu_controller = MainMenuContoller(router)
        player_menu_controller = PlayerMenuController(router)
        player_create_controller = CreatePlayerFormController(router, player_manager)
        player_edit_menu_controller = EditPlayerMenuController(router, player_manager)
        player_edit_form_controller = EditPlayerFormController(router, player_manager)
        tournament_menu_controller = TournamentMenuController(router)
        tournament_create_controller = CreateTournamentFormController(router, tournament_manager)
        tournament_edit_menu_controller = EditTournamentMenuController(router, tournament_manager)
        tournament_edit_form_controller = EditTournamentFormController(router, tournament_manager)
        reports_menu_controller = ReportsMenuController(router)
        player_reports_controller = PlayerReportsController(router, player_manager)
        tournament_reports_menu = TournamentReportsMenuController(router, tournament_manager)
        tournament_reports = TournamentReportsController(router, tournament_manager)
        exit_controller = ExitController(router)
        error_controller = ErrorPageContoller(router)
        not_enough_players_controller = NotEnoughPlayersErrorPageContoller(router)

        router.add_route('/', main_menu_controller)
        router.add_route('/player', player_menu_controller)
        router.add_route('/player/create', player_create_controller)
        router.add_route('/player/edit/menu', player_edit_menu_controller)
        router.add_route('/player/edit/form?', player_edit_form_controller)
        router.add_route('/tournament', tournament_menu_controller)
        router.add_route('/tournament/create', tournament_create_controller)
        router.add_route('/tournament/edit/menu', tournament_edit_menu_controller)
        router.add_route('/tournament/edit/form?', tournament_edit_form_controller)
        router.add_route('/reports', reports_menu_controller)
        router.add_route('/reports/players', player_reports_controller)
        router.add_route('/reports/tournaments', tournament_reports_menu)
        router.add_route('/reports/tournament?', tournament_reports)
        router.add_route('/error', error_controller)
        router.add_route('/notenoughplayers', not_enough_players_controller)
        router.add_route('/exit', exit_controller)

        self.launch = router.start
        self.salvage_app = lambda: router.route('/error')

    def run(self):
        self.launch()

    def display_error_page(self):
        self.salvage_app()
