import json
from typing import Dict

class Settings:
    """Class to manage configuration settings from a JSON file."""

    def __init__(self, config_path: str):
        """
        Initialize Settings with the path to the configuration file.

        Args:
            config_path (str): The path to the configuration JSON file.
        """
        self.config_path = config_path
        self.input_folder_path = ""
        self.trigger_word = ""
        self.ending_word = ""
        self.column_name = ""
        self.column_id = ""
        self.google_sheets_link = ""
        self.google_sheets_tab = ""
        self.google_sheets_username = ""
        self.google_sheets_password = ""
        self._load_config()

    def _load_config(self) -> None:
        """Loads the configuration from the JSON file and sets instance variables."""
        with open(self.config_path, 'r') as file:
            config = json.load(file)
            self.input_folder_path = config.get('input_folder_path', '')
            messages_config = config.get('messages', {})
            self.trigger_word = messages_config.get('trigger_word', '')
            self.ending_word = messages_config.get('ending_word', '')
            self.column_name = messages_config.get('column_name', '')
            self.column_id = messages_config.get('column_id', '')
            sheets_config = config.get('google_sheets', {})
            self.google_sheets_link = sheets_config.get('link', '')
            self.google_sheets_tab = sheets_config.get('tab', '')
            self.google_sheets_username = sheets_config.get('username', '')
            self.google_sheets_password = sheets_config.get('password', '')
