import pywt
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

def main():
  import scipy.io.wavfile as sciwav
  from Wavelets import HaarWavelet
  import numpy as np
  from sys import argv

  if len(argv) == 1:
    geluidje = 'snd/clippie.wav'
  else:
    geluidje = argv[1]

  okke = 0

  #x = np.array([1,2,3,20,41,23,5,12,74,2,35,2,5])
  n, x = sciwav.read( geluidje )
  x_ = np.zeros(x.shape[0])
  if okke:
    cA, cD = pywt.dwt( x, 'haar', mode='zpd' ) #noot: doet maar 1 stapje
    x_ = pywt.idwt( cA, cD, 'haar' )[0:len(x)].astype(x.dtype)
  else:
    steps = -1
    X = HaarWavelet.dwt(x, steps=steps) #noot: doet alle stapjes in 1 keer
    x_ = np.rint(HaarWavelet.idwt( X,steps=steps,m = x.shape[0] )).astype(x.dtype)
    print x, x_



  sciwav.write( geluidje.replace(".wav","_new.wav") , n, x_.astype(x.dtype) )
  #print [int(round(i)) for i in HaarWavelet.idwt(X, m=x.shape[0]) ] #is dit ongeveer `x'? We krijgen helaas afrondingsfouten.
  print sum( x-x_ )

if __name__ == "__main__":
  main()
