import numpy as np
from Wavelets import *

def main():
  x = np.array(
    [[[1,1,1,1],
     [1,1,1,1],
     [1,1,0,1],
     [1,1,1,1]],
    [[1,1,1,1],
     [1,1,1,1],
     [1,1,1,1],
     [1,1,1,1]],
    [[1,1,1,1],
     [1,1,1,1],
     [1,1,2,1],
     [1,1,1,1]],
    [[1,1,1,1],
     [1,1,1,1],
     [1,1,3,1],
     [1,1,1,1]]]
  )
  x_float = x.astype('float')

  wavelet = HaarWavelet

  X = wavelet.dwt(x_float)
  x_ = wavelet.idwt(X)
  print X
  print x_

if __name__ == "__main__":
  main()

