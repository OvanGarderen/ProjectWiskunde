import scipy.io.wavfile as sciwav

from FFT2util import FFT, iFFT
import math, cmath
import numpy, numpy.fft as npfft
from sys import argv

def modulus( z ):
  return math.sqrt(z.real**2 + z.imag**2)

def ar2dict( ar, cutoff ):
  dict = {}
  for x in range(len(ar)):
    if modulus(ar[x]) >= cutoff:
      dict[x] = ar[x]
  return dict

def dict2ar( dict, N):
  mat = []
  for x in range(N):
    i = x
    mat.append( dict[i] if i in dict else 0.0 )
  return mat

def realintar( x ):
    return map(lambda y: int(round(y.real)),x)

if len(argv) == 1:
  geluidje = 'snd/spongebob.wav'
else:
  geluidje = argv[1]

print "converting %s" % (geluidje)

"""
n, x = sciwav.read(geluidje) # n == sample rate; x is een numpy array van getallen
X = FFT(x.tolist()) # X is de FFT
dict = ar2dict( X, 0.0 ) # dict is een lijst van {index: waarde} paren
data = dict2ar( dict, len(x) ) # data is de 'geschoonde' FFT
x_ = iFFT( data ) # x_ is een lijst van getallen
x_ = numpy.array(realintar(x_)[0:len(x)]).astype(x.dtype)
"""
n, x = sciwav.read( geluidje )
X = FFT( list(x) )
dict = ar2dict( X, 0.2 )
print "Compression: %f" % (float(len(dict))/len(X))

data = dict2ar( dict, len(X) )
x_ = numpy.array( map(lambda x: int(x.real),iFFT(data)[0:len(x)]) ).astype( x.dtype )
print x_, x.dtype, x_.dtype


sciwav.write( geluidje.replace(".wav","_new.wav") , n, x_ )
