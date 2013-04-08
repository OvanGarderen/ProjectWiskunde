import scipy.io.wavfile as sciwav
from FFT2util import FFT, iFFT
import math, cmath
import numpy, numpy.fft as npfft

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

n, x = sciwav.read('snd/spongebob.wav')
X = FFT(x.tolist())
dict = ar2dict( X, 0.05 )
data = dict2ar( dict, len(x) )
x_ = iFFT( data )
x_ = numpy.array(realintar(x_)[0:len(x)]).astype(x.dtype)

sciwav.write('snd/spongebob_new.wav', n, x_ )
