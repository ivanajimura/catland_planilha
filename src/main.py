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
        name_id_check = gs_connector.validate_cat_data(cat_id=update["Cód. Simplesvet"], cat_name= update["Nome"], id_col=settings.simplesvet_col, name_col=settings.name_col)
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

        if "Novo nome" in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.name_col, value=valid_update["Novo nome"])
                Logger.log(level = "INFO", message = f"Nome atualizado: {valid_update['Cód. Simplesvet']}: {valid_update['Novo nome']}")

        if "Entrada ONG" in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.ngo_entry_col, value = valid_update["Entrada ONG"])
                Logger.log(level = "INFO", message = f"Entrada ONG atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Entrada ONG']}")

        if "Saída ONG" in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.ngo_exit_col, value = valid_update["Saída ONG"])
                Logger.log(level = "INFO", message = f"Saída ONG atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Saída ONG']}")

        if "Carteirinha de Vacinação" in valid_update.keys():
            if valid_update["Carteirinha de Vacinação"] in settings.valid_bool_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.vaccination_card_col, value=valid_update["Carteirinha de Vacinação"])
                Logger.log(level = "INFO", message = f"Carteirinha de Vacinação atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Carteirinha de Vacinação']}")
            else:
                Logger.log(level = "ERROR", message = f"Carteirinha de Vacinação inválida: {valid_update['Cód. Simplesvet']}: {valid_update['Carteirinha de Vacinação']}")

        if "Data nasc." in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.birthday_col, value = valid_update["Data nasc."])
                Logger.log(level = "INFO", message = f"Data nasc. atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Data nasc.']}")

        if "Gênero" in valid_update.keys():
            if valid_update["Gênero"] in settings.valid_sex_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.sex_col, value=valid_update["Gênero"])
                Logger.log(level = "INFO", message = f"Gênero atualizado: {valid_update['Cód. Simplesvet']}: {valid_update['Gênero']}")
            else:
                Logger.log(level = "ERROR", message = f"Gênero inválido: {valid_update['Cód. Simplesvet']}: {valid_update['Gênero']}")

        if "Raça" in valid_update.keys():
            if valid_update["Raça"] in settings.valid_race_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.race_col, value=valid_update["Raça"])
                Logger.log(level = "INFO", message = f"Raça atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Raça']}")
            else:
                Logger.log(level = "ERROR", message = f"Raça inválida: {valid_update['Cód. Simplesvet']}: {valid_update['Raça']}")
        
        if "Cor" in valid_update.keys():
            if valid_update["Cor"] in settings.valid_color_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.color_col, value=valid_update["Cor"])
                Logger.log(level = "INFO", message = f"Cor atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Cor']}")
            else:
                Logger.log(level = "ERROR", message = f"Cor inválida: {valid_update['Cód. Simplesvet']}: {valid_update['Cor']}")

        if "Castração" in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.date_neuter_col, value = valid_update["Castração"])
                Logger.log(level = "INFO", message = f"Castração atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Castração']}")

        if "FIV" in valid_update.keys():
            if valid_update["FIV"] in settings.valid_fiv_felv_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.FIV_col, value=valid_update["FIV"])
                Logger.log(level = "INFO", message = f"FIV atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['FIV']}")
            else:
                Logger.log(level = "ERROR", message = f"FIV inválida: {valid_update['Cód. Simplesvet']}: {valid_update['FIV']}")
        
        if "FELV" in valid_update.keys():
            if valid_update["FELV"] in settings.valid_fiv_felv_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.FELV_col, value=valid_update["FELV"])
                Logger.log(level = "INFO", message = f"FELV atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['FELV']}")
            else:
                Logger.log(level = "ERROR", message = f"FELV inválida: {valid_update['Cód. Simplesvet']}: {valid_update['FELV']}")

        if "Data Teste FIV e FELV" in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.date_FIV_FELV_col, value = valid_update["Data Teste FIV e FELV"])
                Logger.log(level = "INFO", message = f"Data Teste FIV e FELV atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Data Teste FIV e FELV']}")

        if "Data 2ª Dose Vacina" in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.date_2nd_dose_vaccine_col, value = valid_update["Data 2ª Dose Vacina"])
                Logger.log(level = "INFO", message = f"Data 2ª Dose Vacina atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Data 2ª Dose Vacina']}")

        if "Tipo de Vacina" in valid_update.keys():
            if valid_update["Tipo de Vacina"] in settings.valid_vaccine_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.vaccine_type_col, value=valid_update["Tipo de Vacina"])
                Logger.log(level = "INFO", message = f"Tipo de Vacina atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Tipo de Vacina']}")
            else:
                Logger.log(level = "ERROR", message = f"Tipo de Vacina inválida: {valid_update['Cód. Simplesvet']}: {valid_update['Tipo de Vacina']}")

        if "Renovação Vacina" in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.date_vaccine_renew_col, value = valid_update["Renovação Vacina"])
                Logger.log(level = "INFO", message = f"Renovação Vacina atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Renovação Vacina']}")

        if "Raiva" in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.date_rabies_vaccine_col, value = valid_update["Raiva"])
                Logger.log(level = "INFO", message = f"Raiva atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Raiva']}")
        
        if "Renovação Raiva" in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.date_rabies_renew_col, value = valid_update["Renovação Raiva"])
                Logger.log(level = "INFO", message = f"Renovação Raiva atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Renovação Raiva']}")
        
        if "História" in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.history_col, value = valid_update["História"])
                Logger.log(level = "INFO", message = f"História atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['História']}")
        
        if "Família" in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.family_col, value = valid_update["Família"])
                Logger.log(level = "INFO", message = f"Família atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Família']}")

        if "Observação" in valid_update.keys():
            if True:
                gs_connector.append_data_to_cell(row_number = row_number, col_letter=settings.notes_col, additional_value = valid_update["Observação"])
                Logger.log(level = "INFO", message = f"Observação atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Observação']}")

        if "Microchip" in valid_update.keys():
            if valid_update["Microchip"] in settings.valid_bool_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.microchip_col, value=valid_update["Microchip"])
                Logger.log(level = "INFO", message = f"Microchip atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Microchip']}")
            else:
                Logger.log(level = "ERROR", message = f"Microchip inválida: {valid_update['Cód. Simplesvet']}: {valid_update['Microchip']}")

        if "Interações com outros animais" in valid_update.keys():
            if valid_update["Interações com outros animais"] in settings.valid_bool_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.interaction_animals_col, value=valid_update["Interações com outros animais"])
                Logger.log(level = "INFO", message = f"Interações com outros animais atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Interações com outros animais']}")
            else:
                Logger.log(level = "ERROR", message = f"Interações com outros animais inválida: {valid_update['Cód. Simplesvet']}: {valid_update['Interações com outros animais']}")

        if "Interação com Humanos" in valid_update.keys():
            if valid_update["Interação com Humanos"] in settings.valid_bool_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.interaction_humans_col, value=valid_update["Interação com Humanos"])
                Logger.log(level = "INFO", message = f"Interação com Humanos atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Interação com Humanos']}")
            else:
                Logger.log(level = "ERROR", message = f"Interação com Humanos inválida: {valid_update['Cód. Simplesvet']}: {valid_update['Interação com Humanos']}")


        if "Perfil" in valid_update.keys():
            if valid_update["Perfil"] in settings.valid_profile_list:
                gs_connector.update_value(row_number = row_number, col_letter=settings.profile_col, value=valid_update["Perfil"])
                Logger.log(level = "INFO", message = f"Perfil atualizado: {valid_update['Cód. Simplesvet']}: {valid_update['Perfil']}")
            else:
                Logger.log(level = "ERROR", message = f"Perfil inválido: {valid_update['Cód. Simplesvet']}: {valid_update['Perfil']}")

        if "Devolução" in valid_update.keys():
            if True:
                gs_connector.update_value(row_number = row_number, col_letter=settings.returned_col, value = "Sim")
                gs_connector.update_value(row_number = row_number, col_letter=settings.reason_returned_col, value = valid_update["Motivo"])
                gs_connector.update_value(row_number = row_number, col_letter=settings.date_returned_col, value = str(valid_update["Devolução"]))
                Logger.log(level = "INFO", message = f"Devolução atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Devolução']} {valid_update['Motivo']}")

        if "Observação saúde" in valid_update.keys():
            if True:
                gs_connector.append_data_to_cell(row_number = row_number, col_letter=settings.health_notes_col, additional_value = valid_update["Observação saúde"])
                Logger.log(level = "INFO", message = f"Observação saúde atualizada: {valid_update['Cód. Simplesvet']}: {valid_update['Observação saúde']}")


if __name__ == "__main__":
    main()
