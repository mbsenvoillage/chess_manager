import os, sys
from typing import Dict
import os
from dotenv import load_dotenv

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

load_dotenv()


class ViewContentLoader:
    """Loads content from data store into instance of view"""
    from store import static_view_content, app_data
    from View.view import View

    static_content: Dict = static_view_content
    app_data: Dict = app_data
    view_attribute_to_be_dynamically_built = os.getenv('KEY_FOR_DYNAMIC_VIEW_DATA')
    
    def plug_selectable_option_builder(self, builder, view_entry_to_populate):
        self.__setattr__('option_builder', builder)
        return self

    def unplug_selectable_option_builder(self):
        self.__delattr__('option_builder')

    def load_content(self, view: View, key: str):
        for attribute in view.get_own_attributes():
            setattr(view, attribute, self.static_content[key][attribute])
        if hasattr(self, 'option_builder'):
            setattr(view, self.view_attribute_to_be_dynamically_built, self.option_builder.build_view_options())
            self.unplug_selectable_option_builder()
        return 
