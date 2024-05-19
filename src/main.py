from src.helper.settings import Settings
from src.helper.file_helper import FileHelper
from src.helper.updater import Updater
from src.helper.google_sheets_connector import GoogleSheetsConnector
from src.helper.logger import Logger

def main():
    
    # Load settings
    settings = Settings("config/settings.json")
    Logger.log(level="INFO", message="Configurações carregadas.")

    # Removing old log file:
    FileHelper.remove_file_if_exists(settings.log_file_path)
    Logger.log(level="INFO", message="Arquivo de log antigo removido.")

    # Initialize FileHelper and Updater
    file_helper = FileHelper(settings)
    updater = Updater(settings)

    # Read files from the input folder
    Logger.log(level="INFO", message = f"Lendo arquivos da pasta {settings.input_folder_path}...")
    file_helper.read_files()
    file_contents = file_helper.get_contents()
    Logger.log(level="INFO", message = f"Arquivos da pasta {settings.input_folder_path} lidos com sucesso.")
    

    # Parse updates from file contents
    Logger.log(level="INFO", message = f"Processando mensagens...")
    for content in file_contents:
        Logger.log(level="INFO", message = f"Mensagem em análise: {content}.")
        updates = updater.parse_updates(content)
        if updates:
            Logger.log(level="INFO", message=f"Atualizações encontradas:{updates}")
        else:
            Logger.log(level="WARNING", message=f"Nenhuma atualização encontrada")
    
    # Connect to Google Sheets
    Logger.log(level="INFO", message=f"Conectando ao Google Planilhas...")
    try:
        gs_connector = GoogleSheetsConnector(
                                        credentials_path=settings.credentials_path,
                                        spreadsheet_id=settings.google_sheets_id,
                                        sheet_name=settings.google_sheets_tab)
        Logger.log(level="INFO", message=f"Conexão ao Google Planilhas realizada.")
    except Exception as e:
        Logger.log(level="ERROR", message = f"Erro ao conectar ao Google Planilhas: {e}")
    
    # Checking if names and ids match (this is a common error)
    Logger.log(level="INFO", message=f"Verificando se ids e nomes estão corretos...")
    valid_updates = []
    invalid_updates = []
    for update in updates:
        name_id_check = gs_connector.validate_cat_data(cat_id=update["Cód. Simplesvet"], cat_name= update["Nome"], id_col=settings.simplesvet_col, name_col=settings.nome_col)
        if not name_id_check:
            invalid_updates.append(update)
            Logger.log(level = "ERROR", message=f"Nome e id não batem com planilha: {update}. Atualização não será realizada.")
        if name_id_check:
            valid_updates.append(update)
            Logger.log(level="INFO", message = f"Esta atualização será realizada: {update}")
    Logger.log(level="INFO", message = f"Estas atualizações serão realizadas: {valid_updates}")
    Logger.log(level="WARNING", message = f"Estas atualizações NÃO serão realizadas: {invalid_updates}")

    # Updating items
    for valid_update in valid_updates:
        row_number = gs_connector.get_row_from_data(pattern = valid_update["Cód. Simplesvet"], col = settings.simplesvet_col)
        if "Local" in valid_update.keys():
            if valid_update["Local"] in settings.valid_local_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.local_col, value=valid_update["Local"])
                Logger.log(level = "INFO", message = f"Local atualizado: {valid_update['Cód. Simplesvet']}: {valid_update['Local']}")
            else:
                Logger.log(level = "ERROR", message = f"Local inválido: {valid_update['Cód. Simplesvet']}: {valid_update['Local']}")

        if "Status" in valid_update.keys():
            if valid_update["Status"] in settings.valid_status_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.status_col, value=valid_update["Status"])
                Logger.log(level = "INFO", message = f"Status atualizado: {valid_update['Cód. Simplesvet']}: {valid_update['Status']}")
            else:
                Logger.log(level = "ERROR", message = f"Status inválido: {valid_update['Cód. Simplesvet']}: {valid_update['Status']}")

        if "Gênero" in valid_update.keys():
            if valid_update["Gênero"] in settings.valid_sex_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.sex_col, value=valid_update["Gênero"])
                Logger.log(level = "INFO", message = f"Gênero atualizado: {valid_update['Cód. Simplesvet']}: {valid_update['Gênero']}")
            else:
                Logger.log(level = "ERROR", message = f"Gênero inválido: {valid_update['Cód. Simplesvet']}: {valid_update['Gênero']}")

        if "Novo nome" in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.nome_col, value=valid_update["Novo nome"])
                Logger.log(level = "INFO", message = f"Nome atualizado: {valid_update['Cód. Simplesvet']}: {valid_update['Novo nome']}")
        
        if "Observação saúde" in valid_update.keys():
            if True:
                gs_connector.append_data_to_cell(row_number = row_number, col_letter=settings.health_notes_col, additional_value = valid_update["Observação saúde"])
                Logger.log(level = "INFO", message = f"Observação saúde atualizado: {valid_update['Cód. Simplesvet']}: {valid_update['Observação saúde']}")

if __name__ == "__main__":
    main()
