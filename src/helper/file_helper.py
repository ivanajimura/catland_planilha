import os
import json
from typing import List

class FileHelper:
    """Helper class to manage file operations in the input folder."""

    def __init__(self, config_path: str):
        """
        Initialize FileHelper with the path to the configuration file.

        Args:
            config_path (str): The path to the configuration JSON file.
        """
        self.config_path = config_path
        self.contents = []
        self._load_config()

    def _load_config(self) -> None:
        """Loads the configuration from the JSON file."""
        with open(self.config_path, 'r') as file:
            config = json.load(file)
            self.folder_path = config['input_folder_path']

    def read_files(self) -> None:
        """Reads all text files in the folder and stores their contents in a variable."""
        self.contents.clear()
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".txt"):
                with open(os.path.join(self.folder_path, filename), 'r') as file:
                    self.contents.append(file.read())

    def remove_files(self) -> None:
        """Removes all text files in the folder."""
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".txt"):
                os.remove(os.path.join(self.folder_path, filename))

    def get_contents(self) -> List[str]:
        """
        Get the contents read from the files.

        Returns:
            List[str]: List of strings containing the contents of each file.
        """
        return self.contents
