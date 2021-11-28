from manager import PlayerManager, TournamentManager
from Router.router import Router
from Controllers.controllers import CreatePlayerFormController, CreateTournamentFormController, EditPlayerFormController, EditPlayerMenuController, EditTournamentFormController, EditTournamentMenuController, ExitController, MainMenuContoller, PlayerMenuController, PlayerReportsController, ReportsMenuController, TournamentMenuController, TournamentReportsMenuController

class App():

    launch: callable

    def __init__(self) -> None:
        router = Router()
        player_manager = PlayerManager()
        tournament_manager = TournamentManager(player_manager)

        main_menu_controller = MainMenuContoller(router)
        player_menu_controller = PlayerMenuController(router)
        player_create_controller = CreatePlayerFormController(router,player_manager)
        player_edit_menu_controller = EditPlayerMenuController(router,player_manager)
        player_edit_form_controller = EditPlayerFormController(router,player_manager)
        tournament_menu_controller = TournamentMenuController(router)
        tournament_create_controller = CreateTournamentFormController(router,tournament_manager)
        tournament_edit_menu_controller = EditTournamentMenuController(router,tournament_manager)
        tournament_edit_form_controller = EditTournamentFormController(router,tournament_manager)
        reports_menu_controller = ReportsMenuController(router)
        player_reports_controller = PlayerReportsController(router,player_manager)
        tournament_reports_menu = TournamentReportsMenuController(router,tournament_manager)
        exit_controller = ExitController(router)

        router.add_route('/',main_menu_controller)
        router.add_route('/player',player_menu_controller)
        router.add_route('/player/create',player_create_controller)
        router.add_route('/player/edit/menu',player_edit_menu_controller)
        router.add_route('/player/edit/form?', player_edit_form_controller)
        router.add_route('/tournament',tournament_menu_controller)
        router.add_route('/tournament/create',tournament_create_controller)
        router.add_route('/tournament/edit/menu',tournament_edit_menu_controller)
        router.add_route('/tournament/edit/form?',tournament_edit_form_controller)
        router.add_route('/reports',reports_menu_controller)
        router.add_route('/reports/players',player_reports_controller)
        router.add_route('/reports/tournaments',tournament_reports_menu)
        router.add_route('/exit', exit_controller)

        self.launch = router.start

    def run(self):
        self.launch()
