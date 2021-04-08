import sys
from os import mkdir
from os.path import join, isdir
from rw.ht_reader import *
from fht.fht import *
from fht.compare import *
from fht.average import *
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

# TYPE of operation
# TYPE = sys.argv[1]

# VISUALIZATION_APP = "http://localhost:9000"

# offset = open(int('D:\\this.gif', 'rb')).read()


def safeMkdir(path):
    if not isdir(path):
        mkdir(path)

# Método criado para teste rápido, aqui será criado previamente a assinatura padrão para teste
def runFHT():
    # SFILE_PATH = sys.argv[2]
    # OFFSET = int(sys.argv[3])

    OP_PATH = 'C:/Users/junior/Documents/test/computado/out.txt'
    SFILE_PATH = "C:/Users/junior/Documents/teste/test.gif"
    OFFSET = 16

    '''
    safeMkdir(join("D:\\CODE\\scripts python\\alg_fht\\teste", "fht"))
    fileName = "computed"
    OP_PATH = join("D:\\CODE\\scripts python\\alg_fht\\teste", "fht", str(fileName))
    '''

    r = HTFileReader(SFILE_PATH, OFFSET)
    fht = FHTAnalyzer(OFFSET)
    r.read(fht.compute)
    print(np.matrix(fht.signature()[0]))
    print('\n')
    print(np.matrix(fht.signature()[1]))
    f = open(OP_PATH, "w+")
    f.write(str(fht))
    f.close()


'''
    print(" ------ FHT Matrix Computed ------ ")
    print(" The FHT matrix has been saved in {0} ".format(OP_PATH))
    print(" RUN: cp ./output/fht/{0} WEBAPP_PATH/data/computed/fht/".format(fileName))
    print(" You can view the visualization at {0}#/visualize/fht/{1}/{2}".format(VISUALIZATION_APP, OFFSET, fileName))
    print(" ------ VISUALIZATION READY ------ ")
'''

# Neste método será feito a correlação
def runFHTC():
    SFILE_PATH = 'C:/Users/junior/Documents/teste/test.gif'
    CFILE_PATH = 'C:\\Users\\junior\\Documents\\teste\\8.gif'
    OP_PATH = 'C:/Users/junior/Documents/test/computado/out.txt'
    OFFSET = 16

    '''
    safeMkdir(join("output", "fht"))
    fileName = "correlation"
    OP_PATH = join("output", "fht", str(fileName))
    '''
	# gera a primeira assinatura
    r1 = HTFileReader(SFILE_PATH, OFFSET)
    fht1 = FHTAnalyzer(OFFSET)
    r1.read(fht1.compute)
	
	# Gera a segunda assinatura
    r2 = HTFileReader(CFILE_PATH, OFFSET)
    fht2 = FHTAnalyzer(OFFSET)
    r2.read(fht2.compute)

    print(np.matrix(fht1.signature()[0]))
    print()
    print(np.matrix(fht2.signature()[0]))
    print()
	
	# correlaciona as assinaturas, neste caso são só duas assinaturas random, para uma correlação certa uma das assinaturas 
	# teria que ser a padrão, neste caso a fht1 seria a previamente criada e o fht2 seria um arquivo random escolhido para testar sua correlação.
    cm = CompareFHT(fht1.signature(), fht2.signature())
    print(cm.correlate())
    p = cm.assuranceLevel()
    print('{:.1%}'.format(p))

	# Os métodos abaixo sao a entrada para gerar a assinatura padrão. 
	# É juntado as assinaturas criando uma so que sera usada para comparar os arquivos escolhidos.
    avg = FHTAverage(fht1.signature(), 1)
    avg = avg.accumulate(fht2.signature())

    f = open(OP_PATH, "w+")
    f.write(str(avg))
    f.close()


'''
    print(" ------ FHT Correlation Computed ------ ")
    print(" The FHT matrix has been saved in {0} ".format(OP_PATH))
    print(" THE Assurance Level for the 2 files is : {0}".format(cm.assuranceLevel()))
    print(" RUN: cp ./output/fht/{0} WEBAPP_PATH/data/computed/fht/".format(fileName))
    print(" You can view the visualization at {0}#/visualize/fht/{1}/{2}".format(VISUALIZATION_APP, OFFSET, fileName))
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

runFHTC()
