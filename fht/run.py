# -*- coding: latin-1 -*-

from rw.ht_reader import *
from fht.fht import *
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)
from fht.compare import *
import time

# File Header Trailer Analysis

OFFSET = 4
r = HTFileReader("/home/guilherme/Área de Trabalho/Workspace Guilherme/TCC - Análise e assinatura de arquivos/code/test-files/teste.gif", OFFSET)
fht = FHTAnalyzer(OFFSET)
r.read(fht.compute)
print(np.matrix(fht.signature()[0]))
print('\n')
print(np.matrix(fht.signature()[1]))


# File Header Trailer Assurance Level
'''
cm = CompareFHT(fht1.signature(), fht2.signature())
print(cm.correlate())
print(cm.assuranceLevel())
'''
# Note: Assurance level returns the __MEAN__ not the __MAX__ as specified here.
