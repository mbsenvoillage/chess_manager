from view import ContentLoader, Menu
import manager

def quit_app():
    exit()

view_manager = manager.ViewManager()
main_menu = Menu(view_manager, ContentLoader(), 'MAIN_MENU')
player_menu = Menu(view_manager, ContentLoader(), 'PLAYER_MENU')
edit_player = Menu(view_manager, ContentLoader('player'), 'PLAYER_EDIT')
tournament_menu = Menu(view_manager, ContentLoader(), 'TOURNAMENT_MENU')
route_map = {'/': main_menu, '/player': player_menu, '/player/edit': edit_player, '/tournament': tournament_menu, '/exit': quit_app}
view_manager.__setattr__('route_map', route_map)



main_menu.render()