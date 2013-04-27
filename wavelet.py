import pywt
import numpy as np
from math import sqrt

def test2d():
  from Wavelets import HaarWavelet
  import numpy as np
  x = np.array(
      [ [1,1,1,1],
        [1,1,1,1],
        [1,1,1,1],
        [1,1,1,1] ]
  )
  X = HaarWavelet.next_2d(x)
  Y = pywt.dwt2( x, 'haar' )
  Z = pywt.dwt2( Y[0], 'haar' )
  print Y, Z
  print X

def ar2dict( ar, cutoff ):
  dict = {}
  for x in range(len(ar)):
    if abs(ar[x]) >= cutoff:
      dict[x] = ar[x]
  return dict

def dict2ar( dict, N):
  ar = np.zeros(N)
  for i in range(N):
    ar[i] = dict[i] if i in dict else 0.0
  return ar

def find_cutoff( ar, ratio ):
  if ratio > 1 or ratio < 0:
    print "fuck off biatch"
    assert 0

  a = np.sort(np.absolute(ar))
  return a[int((1-ratio)*len(ar))]

def main():
  import scipy.io.wavfile as sciwav
  from Wavelets import HaarWavelet
  from sys import argv

  if len(argv) == 1:
    geluidje = 'snd/clippie.wav'
  else:
    geluidje = argv[1]

  okke = 0
  geluid = 1

  x = np.zeros(1)
  if geluid:
    n, x = sciwav.read( geluidje )
  else:
    x = np.array([1,2,3,20,41,23,5,12,74,2,35,2,5])
  x_ = np.zeros(x.shape[0])
  if okke:
    cA, cD = pywt.dwt( x, 'haar', mode='zpd' ) #noot: doet maar 1 stapje
    x_ = pywt.idwt( cA, cD, 'haar' )[0:len(x)].astype(x.dtype)
  else:
    steps = -1
    X = HaarWavelet.dwt(x, steps=steps) #noot: doet alle stapjes in 1 keer
    #print X
    cutoff = find_cutoff(X, 0.01)
    print cutoff
    dict = ar2dict( X, cutoff )
    #print "dict = ", dict
    print "Compression: %f" % (float(len(dict))/len(X))
    data = dict2ar( dict, len(X) )
    x_ = np.rint(HaarWavelet.idwt( data,steps=steps,m = x.shape[0] )).astype(x.dtype)
    print x, x_

  if geluid:
    sciwav.write( geluidje.replace(".wav","_new.wav") , n, x_.astype(x.dtype) )
  else:
    print [int(round(i)) for i in HaarWavelet.idwt(X, m=x.shape[0]) ] #is dit ongeveer `x'? We krijgen helaas afrondingsfouten.
  print sum( x-x_ )

if __name__ == "__main__":
  main()
