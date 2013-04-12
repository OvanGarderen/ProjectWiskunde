from FFT2util import *
from DFTutil import *
from WVGutil import *
import math, cmath, sys

def modulus( z ):
  return math.sqrt(z.real**2 + z.imag**2)

def mat2dict( mat, cutoff ):
  N,M = (len(mat),len(mat[0]))
  dict = {}
  for y in range(N):
    for x in range(M):
      if modulus(mat[y][x]) >= cutoff:
        dict[y*N + x] = mat[y][x]
  return dict

def dict2mat( dict, N, M ):
  mat = []
  for y in range(N):
    matrow = []
    for x in range(M):
      i = y*N + x
      matrow.append( dict[i] if i in dict else 0.0 )
    mat.append(matrow)
  return mat

def realintar( x ):
    return map(lambda y: int(round(y.real)),x)


if __name__ == "__main__":

  data, (N, M) = img2mat( "plaatjes/smile.png" )
  
  mat = FFT2D( data )
  dict = mat2dict(mat, float(sys.argv[1]) )
  
  print len(dict)
  
  wvg_save_v2( dict, (N,M), "plaatjes/smilec="+sys.argv[1]+".wvg" )
  dict, (N,M) = wvg_open_v2( "plaatjes/smilec="+sys.argv[1]+".wvg" )
  
  mat_new = dict2mat(dict, N, M )
  data_new = iFFT2D( mat_new )
  
#dit is dus gefixt nu, het lag toch aan het algo idd
#for y in range(N):
#  for x in range(M):
#    pass
#    data_new[y][x] *= N
  
  print len(data_new) * len(data_new[0]), N*M
  data_new = matslice( data_new, (N,M))
  print len(data_new) * len(data_new[0]), N*M
  
  mat2img(realintmat(data_new), (N,M) ).save("plaatjes/Usmilec="+sys.argv[1]+".jpg")
  
  
#mat2img(realintmat( iFFT2D(mat_new) ), (N, M)).save("plaatjes/Usmile.jpg")
