import numpy as np
from Wavelet_Defs import wavelet_dict

wave = wavelet_dict['db2']

dataset = np.array(
    [2,-16,6,1,
     5,1,-9,10]
).astype('float')

enc = wave.dwt(dataset,steps=1)

print enc

dec = wave.idwt(enc,steps=1)

print dataset
print "-->"
print dec
