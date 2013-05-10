import pywt
import numpy as np

def main():
  import scipy.io.wavfile as sciwav
  from Wavelets import HaarWavelet, Daubechies2Wavelet

  steps = 1
  x = np.array([1,1,1,1,1,1,1,1])
  x_float = x.astype('float')

  X = Daubechies2Wavelet.dwt(x_float, steps=1)
  cA, cD = pywt.dwt( x, 'db2', mode='zpd' ) #noot: doet maar 1 stapje
  print "Onze implementatie:\n",X
  print "Pywt:\n",cA, cD
  print
  print "Onze implementatie geeft terug:\n",Daubechies2Wavelet.idwt(X,steps=1)
  print "Pywt:\n",pywt.idwt(cA,cD,'db2',mode='zpd')

if __name__ == "__main__":
  main()
