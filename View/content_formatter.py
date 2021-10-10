def view_selectable_options_formatter(options):
    formatted_text = ''
    for option in options:
        formatted_text += option['text'] + '\n'
    return formatted_text

def view_info_formatter(pieces_of_info):
    formatted_text = ''
    for info in pieces_of_info:
        formatted_text += info + '\n'
    return formatted_text
