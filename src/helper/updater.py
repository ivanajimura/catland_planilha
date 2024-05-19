from typing import Dict, List
from .settings import Settings

class Updater:
    """Class to parse updates from text files."""

    def __init__(self, settings: Settings):
        """
        Initialize Updater with the Settings instance.

        Args:
            settings (Settings): An instance of the Settings class.
        """
        self.settings = settings

    def parse_updates(self, file_contents: str) -> List[Dict[str, str]]:
        """
        Parse updates from file contents between trigger and ending words.

        Args:
            file_contents (str): Contents of the text file.

        Returns:
            List[Dict[str, str]]: List of dictionaries containing parsed updates.
        """
        trigger_word = self.settings.trigger_word
        ending_word = self.settings.ending_word
        updates = []
        start_index = file_contents.find(trigger_word)
        while start_index != -1:
            end_index = file_contents.find(ending_word, start_index + len(trigger_word))
            if end_index != -1:
                update_data = self._parse_message(file_contents[start_index:end_index])
                if update_data:
                    updates.append(update_data)
                start_index = file_contents.find(trigger_word, end_index)
            else:
                break
        return updates

    def _parse_message(self, message: str) -> Dict[str, str]:
        """
        Parse a single message and extract relevant data into a dictionary.

        Args:
            message (str): The message to parse.

        Returns:
            Dict[str, str]: A dictionary containing parsed data.
        """
        lines = message.split('\n')
        data = {}
        for line in lines:
            if line.startswith("Nome:"):
                data["Nome"] = line.split(":")[1].strip()
            elif line.startswith("Cód. Simplesvet:"):
                data["Cód. Simplesvet"] = line.split(":")[1].strip()
            elif line.startswith("Status:"):
                data["Status"] = line.split(":")[1].strip()
            # Add more conditions for other data to parse if needed
        return data