import pywt
import numpy as np
from Wavelets import *

def main():
  import scipy.io.wavfile as sciwav

  steps = 1
  x = np.array([1,1,1,1,1,1,0,1])
  x_float = x.astype('float')

  wavelet = HaarWavelet

  X = wavelet.dwt(x_float)
  x_ = wavelet.idwt(X)
  #//cA, cD = pywt.dwt( x, 'db2', mode='zpd' ) #noot: doet maar 1 stapje
  print X, x_

if __name__ == "__main__":
  main()
