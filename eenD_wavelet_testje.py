import numpy as np
import pywt
from Wavelet_Defs import wavelet_dict

wave = wavelet_dict['db2']

dataset = np.array(
    [25,10,3,-5,7,12,33,4]
).astype('float')

enc = wave.dwt(dataset)
dec = wave.idwt(enc)

print
print
print dataset
print " -> encoding step = 1"
print enc
print dec

print "pywt geeft:"
ca,cd = pywt.wavedec(dataset, 'db2')
lal = np.concatenate((ca,cd))
print lal
