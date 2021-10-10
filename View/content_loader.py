from typing import Dict
from store import static_view_content, app_data

class ViewContentLoader:
    """Loads content from data store into instance of view"""
    from View.view import View

    static_content: Dict = static_view_content
    app_data: Dict = app_data
    
    def plug_option_builder(self, builder, view_entry_to_populate):
        self.__setattr__('option_builder', builder)
        self.__setattr__('view_entry_to_populate', view_entry_to_populate)
        return self

    def unplug_option_builder(self):
        self.__delattr__('option_builder')
        self.__delattr__('view_entry_to_populate')

    def load_content(self, view: View, key: str):
        for attribute in view.get_own_attributes():
            print(attribute)
            setattr(view, attribute, self.static_content[key][attribute])
        if hasattr(self, 'option_builder'):
            setattr(view, self.view_entry_to_populate, self.option_builder.build_view_options())
            self.unplug_option_builder()
        return 

