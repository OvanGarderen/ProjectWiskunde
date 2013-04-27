from Wavelets import HaarWavelet
from channels import *
from sys import argv
from FFT2util import FFT2D,iFFT2D,matslice,realintmat
from FFTjan import mat2dict,dict2mat
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

def mat5dict( mat, cutoff ):
  N,M = (len(mat),len(mat[0]))
  dict = {}
  for y in range(N):
    for x in range(M):
      if abs(mat[y][x]) >= cutoff:
        dict[y*N + x] = mat[y][x]
  return dict

def dict5mat( dict, N, M ):
  mat = np.zeros((M,N))
  for y in range(N):
    for x in range(M):
      i = y*N + x
      mat[x][y] = dict[i] if i in dict else 0.0
  return mat

def find_cutoff( ar, ratio ):
  if ratio > 1 or ratio < 0:
    print "fuck off biatch"
    assert 0

  a = np.sort(np.absolute(ar))
  return a[int((1-ratio)*len(ar))]

def main():
  data, dim = img3mat(argv[1])
  
  data = np.array(data)
  data_float = data.astype('float')
  
  print "starting encoding of image %s" % (argv[1])
  encoded = map(HaarWavelet.dwt,data_float)
  print "encoding succesfull"

  dim2 = (len(encoded[0][0]),len(encoded[0]))
  print dim2

  print "making dicks"
  dicks = map(lambda x: mat5dict(x,0.0),encoded)
    
  print len(dicks[0])
    
  print map(lambda x: compress(x[0],x[1]), zip(dicks,encoded))

  print "listing dicks"
  lists = map(lambda x: dict5mat(x,dim2[0],dim2[1]),dicks)
  
  lists = np.array(lists)
  
  print "starting decoding"
  decoded = map(HaarWavelet.idwt,lists)

  print "decoding succesfull"
  sliced = map(lambda x: np.rint(x).astype(data.dtype),decoded)

  mat3img(sliced,dim).save(argv[1].replace('.','_new.'))
  
if __name__ == "__main__":
  main()
