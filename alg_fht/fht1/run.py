from alg_fht.fht1.rw.ht_reader import *
from alg_fht.fht1.fht.fht import *
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
from alg_fht.fht1.fht.compare import *
import time

# File Header Trailer Analysis

OFFSET = 4
r = HTFileReader("C:/Users/junior/Documents/teste/test.gif", OFFSET)
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
