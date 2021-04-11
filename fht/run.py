# -*- coding: latin-1 -*-

from fht.fht.fht import *
from fht.reader.ht_reader import *
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)


# File Header Trailer Analysis
def run_fht(input_file, offset):
    r = HTFileReader(input_file, offset)
    fht_res = FHTAnalyzer(offset)
    r.read(fht_res.compute)

    return [fht_res.signature()[0], fht_res.signature()[1]]

'''
cm = CompareFHT(fht1.signature(), fht2.signature())
print(cm.correlate())
print(cm.assuranceLevel())
'''
# Note: Assurance level returns the __MEAN__ not the __MAX__ as specified here.
