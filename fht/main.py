from fht.core.signature import *
from interfaces.db_interface import *
import os


class Main:
    def __init__(self, input_file, offset):
        self.input_file = input_file
        self.offset = offset
        self.initial_signature_file = '/home/guilherme/Área de Trabalho/Workspace Guilherme/TCC - Análise e assinatura de ' \
                                      'arquivos/Banco de dados de extensões/gif/1.gif'
        self.input_file_extension = os.path.splitext(self.input_file)[1].replace('.', '')

        self.db = DataBaseConnection()

    def run_fht_correlate(self):
        sign1 = Signature(self.input_file, self.offset, self.input_file_extension).generate_signature()                 # Gera a assinatura do arquivo de entrada
        sign2 = Signature(self.initial_signature_file, self.offset, self.input_file_extension).generate_signature()     # gera a assinatura do arquivo base

        sign1.compare_to(sign2.get_signature())                                                                         # compara as duas assinaturas para gerar o objeto final da correlação

        self.register_final_signature(sign1)
        self.register_signature_logs(sign1)

        return sign1.last_compare

    def register_final_signature(self, sign):
        self.db.register_final_signature(sign.file_extension, sign.last_compare['final_signature'])

    def register_signature_logs(self, sign):
        self.db.register_signature_log(sign.file_extension, sign.last_compare['assurance'], sign.last_compare['correlation_matrix'], sign.last_compare['final_signature'])

# TODO: pegar assinatura do banco
# TODO: implementar logs
