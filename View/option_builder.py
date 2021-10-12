import re
from typing import List
from store import app_data


class ViewSelectableOptionBuilder():
    """Builds list of options that can be selected in a View. The template variable names must match the attributes of the object needed to be represented as string."""
    string_template: str
    store_data_key: str
    base_route: str
    displayables: List = []

    def __init__(self, string_template, store_data_key, base_route) -> None:
        self.string_template = string_template
        self.store_data_key = store_data_key
        self.base_route = base_route
        self.app_data_to_displayable_text()
        

    def format_func_argument_builder(self, instance_of_class, attributes):
        return {attribute: getattr(instance_of_class, attribute) for attribute in attributes}

    def app_data_to_displayable_text(self):
        """Produces a string representation of data store object attributes from a template"""
        object_attributes_to_be_fetched = self.extract_object_attributes_from_template()
        object_store = app_data[self.store_data_key]
        for instance in object_store:
            format_config = self.format_func_argument_builder(instance, object_attributes_to_be_fetched)
            self.displayables.append(self.string_template.format(**format_config))
        return

    def extract_object_attributes_from_template(self):
        return list(filter(None, re.split('\W+', self.string_template)))
      
    def build_view_options(self):
        """Builds view options"""
        from View.view import ViewOption
        view_options = []
        for option in self.displayables:
            view_options.append(ViewOption(option, self.base_route).represent_self_as_dict())
        return view_options