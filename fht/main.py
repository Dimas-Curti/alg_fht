from fht.core.signature import *
from interfaces.db_interface import *
from interfaces.json_interface import *
from interfaces.gui_interface import *
import os

MARGIN_OF_DIFF = 5


class Main:
    def __init__(self, input_file, offset, reset_database):
        self.input_file = input_file
        self.offset = offset
        self.reset_database = reset_database
        self.input_file_extension = self.get_extension(self.input_file)
        self.input_signature = None
        self.second_level_comparisons = {}
        self.final_graphic = None

        self.db = DataBaseInterface()
        self.json = JsonInterface()
        self.gui = GuiInterface()

    def run_fht_correlate(self):
        if self.db.is_first_run() or self.reset_database:
            self.db.reset_database()
            self.generate_base_signatures_from_folder()

        self.input_signature = Signature(self.input_file, self.offset, self.input_file_extension).generate_signature()  # Gera a assinatura do arquivo de entrada
        old_signature_file = self.db.get_old_base_signature(self.input_file_extension)

        if old_signature_file:
            old_signature = self.json.read(old_signature_file)

            print('Extensão do arquivo de entrada: ', self.input_file_extension)

            self.input_signature.compare_to(old_signature["to_backend"], self.input_file_extension)                     # compara as duas assinaturas para gerar o objeto final da correlação

            print('Comparação com a assinatura no banco de dados: ', self.input_signature.last_compare)

            if self.input_signature.last_compare["assurance"] < 100 - MARGIN_OF_DIFF:
                first_comparison = self.input_signature.last_compare["final_signature"]

                self.compare_to_other_old_signatures()

                self.register_signature_logs(self.input_signature)

                self.gui.generate_second_level_comparison_graphics(self.second_level_comparisons, first_comparison)

                return {
                    'code': 'suspect_file',
                    'fake_extension': self.input_file_extension,
                    'correct_extensions': self.get_correct_extensions()
                }
            else:
                self.register_signature_logs(self.input_signature)
                self.register_final_signature(self.input_signature)

                return {
                    'code': 'success',
                    'correct_extension': self.input_file_extension
                }
        else:
            return {
                'code': 'unknown_extension'
            }

    @staticmethod
    def get_extension(file):
        return os.path.splitext(file)[1].replace('.', '')

    @staticmethod
    def get_extension_by_log_file(file):
        return file[file.index('_') + 1:file.index('.')]\


    def get_correct_extensions(self):
        filtered_data = list(filter(lambda item: item[1] == 100, self.second_level_comparisons.items()))
        correct_extensions = [item[0] for item in filtered_data]

        return correct_extensions

    def register_final_signature(self, sign):
        self.db.register_final_signature(sign.file_extension)

    def register_signature_logs(self, sign):
        json_file_name = self.db.register_signature_log(sign, self.second_level_comparisons)

        if sign.last_compare:
            self.json.write(json_file_name, sign.last_compare['final_signature'])
        else:
            self.json.write(json_file_name, sign.get_signature())

    def generate_base_signatures_from_folder(self):
        folder_path = self.gui.initialize_folder_dialog('Selecione a pasta para gerar assinaturas base')

        for path, subdirs, files in os.walk(folder_path):
            if files is not []:
                for file in files:
                    current_file_extension = self.get_extension(file)
                    current_signature = Signature(os.path.join(path, file), self.offset, current_file_extension).generate_signature()
                    
                    if self.db.has_base_signature(current_file_extension):
                        old_signature_file = self.db.get_old_base_signature(current_file_extension)
                        old_signature = self.json.read(old_signature_file)
                        if old_signature:
                            current_signature.compare_to(old_signature["to_backend"], current_file_extension)

                        self.register_signature_logs(current_signature)
                        self.register_final_signature(current_signature)
                    else:
                        self.register_signature_logs(current_signature)
                        self.register_final_signature(current_signature)

    def compare_to_other_old_signatures(self):
        other_old_signature_files = self.db.get_others_old_base_signatures(self.input_file_extension)

        for other_sign_file in other_old_signature_files:
            other_sign_file = other_sign_file[0]
            other_sign_extension = self.get_extension_by_log_file(other_sign_file)

            other_sign = self.json.read(other_sign_file)
            if other_sign:
                self.input_signature.compare_to(other_sign["to_backend"], other_sign_extension)

                self.second_level_comparisons[self.input_signature.last_compare['compared_extension']] = self.input_signature.last_compare['assurance']
