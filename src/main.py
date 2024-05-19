from src.helper.settings import Settings
from src.helper.file_helper import FileHelper
from src.helper.updater import Updater

def main():
    # Load settings
    settings = Settings("config/settings.json")

    # Initialize FileHelper and Updater
    file_helper = FileHelper(settings)
    updater = Updater(settings)

    # Read files from the input folder
    file_helper.read_files()
    file_contents = file_helper.get_contents()

    # Parse updates from file contents
    for content in file_contents:
        updates = updater.parse_updates(content)
        if updates:
            print("Parsed Updates:", updates)
        else:
            print("No updates found in file.")

if __name__ == "__main__":
    main()
