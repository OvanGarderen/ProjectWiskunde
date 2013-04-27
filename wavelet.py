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
  from Wavelets import HaarWavelet
  import numpy as np
  x = np.array([1,1,1,1])
  cA, cD = pywt.dwt( x, 'db2' ) #noot: doet maar 1 stapje
  X = HaarWavelet.dwt(x) #noot: doet alle stapjes in 1 keer
  #print cA, cD #dus daarom is deze
  print "transform is", X #niet hetzelfde als deze
  print [int(round(i)) for i in HaarWavelet.idwt(X) ] #is dit ongeveer `x'? We krijgen helaas afrondingsfouten.

if __name__ == "__main__":
  test2d()
