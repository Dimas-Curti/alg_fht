from fht.core.signature import *
from interfaces.db_interface import *
from interfaces.json_interface import *
from interfaces.gui_interface import *
import os
import re


class Main:
    def __init__(self, input_file, offset):
        self.input_file = input_file
        self.offset = offset
        self.input_file_extension = self.get_extension(self.input_file)
        self.input_signature = None
        self.second_level_comparisons = {}

        self.db = DataBaseInterface()
        self.json = JsonInterface()
        self.gui = GuiInterface()

    @staticmethod
    def get_extension(file):
        return os.path.splitext(file)[1].replace('.', '')

    @staticmethod
    def get_extension_by_log_file(file):
        return file[file.index('_') + 1:file.index('.')]

    def run_fht_correlate(self):
        if self.db.is_first_run():
            self.generate_base_signatures_from_folder()

        self.input_signature = Signature(self.input_file, self.offset, self.input_file_extension).generate_signature()  # Gera a assinatura do arquivo de entrada
        old_signature_file = self.db.get_old_base_signature(self.input_file_extension)

        if old_signature_file:
            old_signature = self.json.read(old_signature_file)
            self.input_signature.compare_to(old_signature["to_backend"], self.input_file_extension)                     # compara as duas assinaturas para gerar o objeto final da correlação

            self.compare_to_other_old_signatures()

            self.register_signature_logs(self.input_signature)
            self.register_final_signature(self.input_signature)

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
