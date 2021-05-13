from fht.core.signature import *
from interfaces.db_interface import *
from interfaces.json_interface import *
from interfaces.gui_interface import *
import os


class Main:
    def __init__(self, input_file, offset):
        self.input_file = input_file
        self.offset = offset
        self.input_file_extension = self.get_extension(self.input_file[1])

        self.db = DataBaseInterface()
        self.json = JsonInterface()
        self.gui = GuiInterface()

    def run_fht_correlate(self):
        if self.is_first_run():
            self.generate_base_signatures_from_folder()

        sign1 = Signature(self.input_file, self.offset, self.input_file_extension).generate_signature()                 # Gera a assinatura do arquivo de entrada
        old_signature_file = self.db.get_old_base_signature(self.input_file_extension)

        if old_signature_file:
            old_signature = self.json.read(old_signature_file)
            sign1.compare_to(old_signature["to_backend"])                                                               # compara as duas assinaturas para gerar o objeto final da correlação

            self.register_signature_logs(sign1)
            self.register_final_signature(sign1)

            return sign1.last_compare

    def register_final_signature(self, sign):
        self.db.register_final_signature(sign.file_extension)

    def register_signature_logs(self, sign):
        json_file_name = self.db.register_signature_log(sign)

        if sign.last_compare:
            self.json.write(json_file_name, sign.last_compare['final_signature'])
        else:
            self.json.write(json_file_name, sign.get_signature())

    def is_first_run(self):
        return self.db.is_first_run()

    def get_extension(self, file):
        return os.path.splitext(file)[1].replace('.', '')

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
                            current_signature.compare_to(old_signature["to_backend"])

                        self.register_signature_logs(current_signature)
                        self.register_final_signature(current_signature)
                    else:
                        self.register_signature_logs(current_signature)
                        self.register_final_signature(current_signature)
