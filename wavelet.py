import pywt
from math import sqrt

def test2d():
  from Wavelets import HaarWavelet
  import numpy as np
  x = np.array(
    [ [1,2],
      [4,5] ]
  )
  coeffs = pywt.dwt2(x, 'haar')
  X = HaarWavelet.next_2d(x)
  print X
  print HaarWavelet.prev_2d( X )

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
