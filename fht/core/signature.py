from fht.reader.ht_reader import *
from fht.helpers.fht import *
from fht.helpers.compare import *
from fht.helpers.average import *


class Signature:
    def __init__(self, file, offset, extension):
        self.file = file
        self.offset = offset
        self.file_extension = extension

        self.signature = None
        self.last_compare = {}

    def generate_signature(self):
        reader = HTFileReader(self.file, self.offset)
        self.signature = FHTAnalyzer(self.offset)
        reader.read(self.signature.compute)

        return self

    def get_signature(self):
        return {
            "header_signature": self.signature.signature()[0],
            "trailer_signature": self.signature.signature()[1]
        }

    # correlaciona a assinatura do objeto com a assinatura passada como parâmetro para gerar a matriz de correlação e % de precisão da correlação
    # Após isso é acumulada as duas assinaturas e gerada a assinatura média da correlação usada para comparar com os arquivos de entrada.
    def compare_to(self, signature_to_compare, extension_to_compare):
        signature_to_backend = (self.get_signature()["header_signature"], self.get_signature()["trailer_signature"])

        compare = CompareFHT(signature_to_backend, signature_to_compare)
        average = FHTAverage(signature_to_backend, 1)

        self.last_compare['assurance'] = compare.assuranceLevel() * 100
        self.last_compare['compared_extension'] = extension_to_compare
        self.last_compare['final_signature'] = {
            "header_signature": average.accumulate(signature_to_compare).fingerprint()[0],
            "trailer_signature": average.accumulate(signature_to_compare).fingerprint()[1]
        }
        self.last_compare['correlation_matrix'] = {
            'header_correlation': compare.correlate()[0],
            'trailer_correlation': compare.correlate()[1]
        }
