import numpy as np
import pywt
from Wavelet_Defs import wavelet_dict

wave = wavelet_dict['db2']

dataset = np.array(
    [1,2,3,0,1,2,3,4]
).astype('float')

enc = wave.dwt(dataset, steps=1)
dec = wave.idwt(enc, steps = 1)

print
print
print dataset
print " -> encoding step = 1"
print enc
print dec

print "pywt geeft:"
ca,cd = pywt.dwt(dataset, 'db2')
lal = np.concatenate((ca,cd))
print lal
