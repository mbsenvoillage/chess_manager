from view import ContentLoader, Menu
import manager

view_manager = manager.ViewManager()
main_menu = Menu(view_manager, ContentLoader(), 'MAIN_MENU')
player_menu = Menu(view_manager, ContentLoader(), 'PLAYER_MENU')
edit_player = Menu(view_manager, ContentLoader('player'), 'PLAYER_EDIT')
route_map = {'/': main_menu, '/player': player_menu, '/player/edit': edit_player}
view_manager.__setattr__('route_map', route_map)



main_menu.render()