from datetime import datetime
from enum import Enum
from typing import List
from .file_helper import FileHelper
from .settings import Settings


class Logger:
    """Logger class to handle logging messages with different levels and timestamps."""
   
    @staticmethod
    def log(level: str, message: str) -> None:
        """
        Log a message with a given level and timestamp.

        Args:
            level (LogLevel): The level of the log message.
            message (str): The log message.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - {level.upper()} - {message}"
        print(log_message)  # Print the log message to console
        settings = Settings("config/settings.json")
        FileHelper.append_to_file(file_path=settings.log_file_path, content=log_message)

