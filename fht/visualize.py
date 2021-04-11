from os import mkdir
from os.path import join, isdir
from fht.reader.ht_reader import *
from fht.fht.fht import *
from fht.fht.compare import *
from fht.fht.average import *
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)


# Método criado para teste rápido, aqui será criado previamente a assinatura padrão para teste
def run_fht(input_file, offset):
    r = HTFileReader(input_file, offset)
    fht_res = FHTAnalyzer(offset)
    r.read(fht_res.compute)

    return [fht_res.signature()[0], fht_res.signature()[1]]


# Neste método será feito a correlação
def run_fht_correlate(input_file, offset):
    signature_file = '/home/guilherme/Área de Trabalho/Workspace Guilherme/TCC - Análise e assinatura de ' \
                     'arquivos/code/alg_fht/test-files/teste.gif '

    # TODO: implementar logs
    # OP_PATH = 'C:/Users/junior/Documents/test/computado/out.txt'

    # TODO: pegar assinatura do banco
    # gera a assinatura do arquivo base
    r1 = HTFileReader(signature_file, offset)
    fht1 = FHTAnalyzer(offset)
    r1.read(fht1.compute)

    # Gera a assinatura do arquivo de entrada
    r2 = HTFileReader(input_file, offset)
    fht2 = FHTAnalyzer(offset)
    r2.read(fht2.compute)

    # correlaciona as assinaturas, neste caso são só duas assinaturas random, para uma correlação certa uma das
    # assinaturas teria que ser a padrão, neste caso a fht1 seria a previamente criada e o fht2 seria um arquivo
    # random escolhido para testar sua correlação.
    cm = CompareFHT(fht1.signature(), fht2.signature())
    print(cm.correlate())
    p = cm.assuranceLevel()
    print('{:.1%}'.format(p))

    # Os métodos abaixo sao a entrada para gerar a assinatura padrão.
    # É juntado as assinaturas criando uma so que sera usada para comparar os arquivos escolhidos.
    avg = FHTAverage(fht1.signature(), 1)
    avg = avg.accumulate(fht2.signature())

    # retorna matriz de correlação, % de confiança, matriz do header e trailer dos dois arquivos comparados
    return {
        'correlation': cm.correlate(),
        'assurance': '{:.1%}'.format(p),
        'average': str(avg)
    }

    # TODO: implementar logs
    # f = open(OP_PATH, "w+")
    # f.write(str(avg))
    # f.close()


'''
    print(" ------ FHT Correlation Computed ------ ")
    print(" The FHT matrix has been saved in {0} ".format(OP_PATH))
    print(" THE Assurance Level for the 2 files is : {0}".format(cm.assuranceLevel()))
    print(" RUN: cp ./output/fht/{0} WEBAPP_PATH/data/computed/fht/".format(fileName))
    print(" You can web the visualization at {0}#/visualize/fht/{1}/{2}".format(VISUALIZATION_APP, offset, fileName))
    print(" ------ VISUALIZATION READY ------ ")


# CREATE OUTPUT PATH
safeMkdir("output")

if TYPE == "fht":
    runFHT()
elif TYPE == "fhtc":
    runFHTC()

print(" Ensure that you have the visualization engine running as a Grunt JS app ( or ) ")
print(" served as a HTML app via a web server like NGINX ")
# print(" Example-Path to the app: {0} ".format(VISUALIZATION_APP))
'''
