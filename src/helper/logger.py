from datetime import datetime
from enum import Enum
from typing import List
from .file_helper import FileHelper
from .settings import Settings

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class Logger:
    """Logger class to handle logging messages with different levels and timestamps."""

    def __init__(self, settings: Settings):
        """
        Initialize Logger with the Settings instance.

        Args:
            settings (Settings): An instance of the Settings class.
        """
        self.log_file_path = "log.txt"  # Define your log file path
        self.file_helper = FileHelper(settings)

    def log(self, level: LogLevel, message: str) -> None:
        """
        Log a message with a given level and timestamp.

        Args:
            level (LogLevel): The level of the log message.
            message (str): The log message.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - {level.value} - {message}"
        print(log_message)  # Print the log message to console
        self.file_helper.append_to_file(self.log_file_path, log_message)

    def read_logs(self) -> List[str]:
        """
        Read all log messages from the log file.

        Returns:
            List[str]: List of log messages.
        """
        return self.file_helper.read_file(self.log_file_path)
