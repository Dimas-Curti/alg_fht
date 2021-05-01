from fht.reader.ht_reader import *
from fht.helpers.fht import *
from fht.helpers.compare import *
from fht.helpers.average import *
from interfaces.db_interface import *


class Signature:
    def __init__(self, file, offset, extension):
        self.file = file
        self.offset = offset
        self.file_extension = extension

        self.signature = None
        self.last_compare = {}

        self.db = DataBaseConnection()

    def generate_signature(self):
        reader = HTFileReader(self.file, self.offset)
        self.signature = FHTAnalyzer(self.offset)
        reader.read(self.signature.compute)

        return self

    def get_signature(self):
        res = self.signature.signature()
        return res

    # correlaciona a assinatura do objeto com a assinatura passada como parâmetro para gerar a matriz de correlação e % de precisão da correlação
    # Após isso é acumulada as duas assinaturas e gerada a assinatura média da correlação usada para comparar com os arquivos de entrada.
    def compare_to(self, signature_to_compare):
        compare = CompareFHT(self.get_signature(), signature_to_compare)
        average = FHTAverage(self.get_signature(), 1)

        self.last_compare['correlation_matrix'] = str(compare.correlate())
        self.last_compare['assurance'] = compare.assuranceLevel() * 100
        self.last_compare['final_signature'] = str(average.accumulate(signature_to_compare))
