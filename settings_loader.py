from dotenv import load_dotenv
import os

load_dotenv()

def get_default_page_layout():
    return os.getenv('DEFAULT_PAGE_LAYOUT')

def get_default_form_layout():
    return os.getenv('DEFAULT_FORM_LAYOUT')

def get_quit_command():
    return os.getenv('QUIT_COMMAND')

def get_exit_route():
    return os.getenv('QUIT_REDIRECTION_ROUTE')