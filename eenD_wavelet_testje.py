import numpy as np
import pywt
from Wavelet_Defs import wavelet_dict

wave = wavelet_dict['haar']

dataset = np.array(
    [1,2,3,0,1,2,3,4]
).astype('float')

enc = wave.dwt(dataset)


dec = wave.idwt(enc)

print dataset
print enc
print dec

print pywt.dwt(dataset, 'haar')
