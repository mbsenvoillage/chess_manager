from abc import ABC, abstractmethod
import copy
from typing import Union
from manager import PlayerManager, TournamentManager
from Router.router import Router
from settings_loader import get_default_form_layout, get_default_page_layout, get_default_report_layout
from store import static_view_content

class Controller(ABC):
    router: Router
    data_manager: Union[PlayerManager,TournamentManager]
    data_id: str = None

    def __init__(self,router,data_manager=None) -> None:
        super().__init__()
        self.router = router
        self.data_manager = data_manager

    def __call__(self,params):
        if params:
            self.data_id = params
        return self.index(params)

    @abstractmethod
    def index(self,data):
        pass

    def redirect_to(self,route):
        self.router.route(route)
    
    @abstractmethod
    def validate_command(self,command):
        pass

class ExitController(Controller):

    def index(self,data):
        from view import ExitPage
        exit_page_content = static_view_content['EXIT']
        layout = "\n \n{0} \n \n \n{1} \n"
        return ExitPage(self, layout, *exit_page_content.values()).render()

    def validate_command(self, command):
        pass

    def exit(self):
        import os
        os.system('cls' if os.name == 'nt' else 'reset')
        exit()

class ReportController(Controller):
    
    @abstractmethod
    def index(self, data):
        pass
    
    @abstractmethod
    def validate_command(self, command):
        pass

    @abstractmethod
    def search(self,search_criteria):
        pass

class FormController(Controller):
    
    @abstractmethod
    def index(self, data):
        pass
    
    @abstractmethod
    def validate_command(self, command):
        pass

    @abstractmethod
    def validate_input(self,input,field_type):
        pass

    @abstractmethod
    def submit(self,inputs):
        pass

class MainMenuContoller(Controller):
    
    def index(self,data):
        from view import Menu
        main_menu_content = static_view_content['MAIN_MENU']
        return Menu(self, get_default_page_layout(), *main_menu_content.values()).render()

    def validate_command(self, command):
        pass

class PlayerMenuController(Controller):
    
    def index(self, data):
        from view import Menu
        player_menu_content = static_view_content['PLAYER_MENU']
        return Menu(self, get_default_page_layout(), *player_menu_content.values()).render()

    def validate_command(self, command):
        pass

class TournamentMenuController(Controller):
    
    def index(self, data):
        from view import Menu
        tournament_menu_content = tournament_menu_content = static_view_content['TOURNAMENT_MENU']
        return Menu(self, get_default_page_layout(), *tournament_menu_content.values()).render()

    def validate_command(self, command):
        pass

class ReportsMenuController(Controller):

    def index(self, data):
        from view import Menu
        reports_menu_content = static_view_content['REPORTS_MENU']
        return Menu(self, get_default_page_layout(), *reports_menu_content.values()).render()

    def validate_command(self, command):
        pass

class PlayerReportsController(ReportController):

    def index(self, data):
        from view import Report
        player_reports_table_headers =['Last Name', 'First Name', 'Ranking', 'Birthdate']
        players = data if data else [[player.last_name,player.first_name,player.ranking,player.birthdate] for player in self.data_manager.get_all(order_by='alpha')]
        reports_menu_player_content = static_view_content['REPORTS_MENU_PLAYER']
        return Report(self, get_default_report_layout(), *reports_menu_player_content.values(),players,player_reports_table_headers).render()

    def validate_command(self, command):
        pass

    def search(self, search_criteria: str):
        order_by = list(filter(bool,search_criteria.split('/')))[0]
        players = [[player.last_name,player.first_name,player.ranking,player.birthdate] for player in self.data_manager.get_all(order_by)]
        self.index(players)

class TournamentReportsMenuController(Controller):
   
    def index(self, data):
        from view import Menu
        tournaments_reports_content = static_view_content['REPORTS_MENU_TOURNAMENT']
        options = self.make_menu_options('/reports/tournament?id=')
        return Menu(self, get_default_page_layout(), *tournaments_reports_content.values(), options).render()

    def validate_command(self, command):
        pass

    def make_menu_options(self,base_route):
        option_list = []
        for index, tournament in enumerate(self.data_manager.get_all()):
            option_list.append([f"{index+1}. {tournament.name} \n\tVenue: {tournament.venue} \n\tStart date: {tournament.start_date} \n\tEnd date: {tournament.end_date}\n", f"{base_route}{tournament.id}"])
        return option_list

class CreatePlayerFormController(FormController):

    def index(self, data):
        from view import Form
        player_create_content = static_view_content['PLAYER_CREATE']
        return Form(self, get_default_form_layout(),*player_create_content.values()).render()

    def validate_command(self, command):
        pass

    def validate_input(self, input,field_type):
        return self.data_manager.validate(input,field_type)

    def submit(self, inputs):
        self.data_manager.add(inputs)

class CreateTournamentFormController(FormController):

    def index(self, data):
        from view import Form, Completer
        tournament_create_content = static_view_content['TOURNAMENT_CREATE']
        players_for_autocomplete = lambda : [repr(player) for player in self.data_manager.player_manager.get_all()]
        return Form(self,get_default_form_layout(),*tournament_create_content.values(), Completer(players_for_autocomplete(),'players')).render()

    def validate_command(self, command):
        pass

    def validate_input(self, input,field_type):
        return self.data_manager.validate(input,field_type)

    def submit(self, inputs):
        self.data_manager.add(inputs)

class EditPlayerMenuController(Controller):

    def index(self, data):
        from view import Menu
        edit_player_menu_content = static_view_content['PLAYER_EDIT_MENU']
        options = self.make_menu_options('/player/edit/form?id=')
        return Menu(self, get_default_page_layout(), *edit_player_menu_content.values(), options).render()

    def validate_command(self, command):
        pass

    def make_menu_options(self,base_route):
        list_of_options = []
        for index, player in enumerate(self.data_manager.get_all()):
            list_of_options.append([f"{index+1}. {player.first_name} {player.last_name}", f"{base_route}{player.id}"])
        return list_of_options

class EditTournamentMenuController(Controller):

    def index(self, data):
        from view import Menu
        tournament_edit_content = static_view_content['TOURNAMENT_EDIT_MENU']
        options = self.make_menu_options('/tournament/edit/form?id=')
        return Menu(self, get_default_page_layout(), *tournament_edit_content.values(), options).render()

    def validate_command(self, command):
        pass

    def make_menu_options(self,base_route):
        option_list = []
        for index, tournament in enumerate(self.data_manager.get_all()):
            option_list.append([f"{index+1}. {tournament.name} - Venue: {tournament.venue}", f"{base_route}{tournament.id}"])
        return option_list

class EditPlayerFormController(FormController):

    def index(self,data):
        from view import FormEdit
        edit_player_form_content = static_view_content['PLAYER_EDIT_FORM']
        form = FormEdit(self, get_default_form_layout(), *edit_player_form_content.values())
        edited_form_fields = self.edit_form(self.data_manager.get_by_id(data),form.form_fields)
        form.form_fields = edited_form_fields
        return form.render()

    def validate_command(self, command):
        pass

    def validate_input(self, input,field_type):
        return self.data_manager.validate(input,field_type)

    def submit(self, inputs):
        self.data_manager.update(inputs,self.data_id)

    def edit_form(self,entity: dict,form_fields):
        fields = copy.deepcopy(form_fields)
        for field in fields:
            key = field.type
            value = entity[key]
            original_field_text = field.text
            field.text = f"{original_field_text}{value}\nNew value : "
        return fields

class EditTournamentFormController(FormController):

    def index(self,data):
        from view import Form
        edit_tournament_form_content = static_view_content['TOURNAMENT_EDIT_FORM']
        form = Form(self, get_default_form_layout(), *edit_tournament_form_content.values(),form_fields=[])
        form_fields = self.make_form(self.data_manager.get_by_id(data))
        form.form_fields = form_fields
        return form.render()

    def validate_command(self, command):
        pass

    def validate_input(self, input,field_type):
        return self.data_manager.validate(input,'match')

    def submit(self, inputs):
        self.data_manager.update(inputs,self.data_id)
    
    def make_form(self,entity: dict):
        from view import FormField
        fields = []
        for idx, match in enumerate(entity['rounds'][-1]['matches']):
            field_params = {'type': f'match{idx+1}'}
            player_one = PlayerManager().get_by_id(match['player_one'])
            player_two = PlayerManager().get_by_id(match['player_two'])
            text = f"{player_one['first_name']} {player_one['last_name']} vs {player_two['first_name']} {player_two['last_name']}\n{player_one['first_name']} {player_one['last_name']}'s score : "
            field_params['text'] = text
            field = FormField(**field_params)
            fields.append(field)
        return fields