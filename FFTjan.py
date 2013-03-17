from FFT2util import *
from DFTutil import *
import math, cmath

def modulus( z ):
  return math.sqrt(z.real**2 + z.imag**2)

def mat2dict( mat ):
  dict = {}
  for y in range(N):
    for x in range(M):
      if modulus(mat[y][x]) >= 0.0:
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

#dit print dus, tegen m'n verwachting in, niet de matrix zelf terug.
#je doet gekke FFT-fu op regel 21 en 22 van FFT2util die ik niet snap
#ligt dat trouwens aan mij of niet? want het lijkt niet op het algo van die
#pagina.
#maar goed, het algo gaat iets mis in. Misschien dat daarom alles kapoet is
print iFFT2D(FFT2D([[.5,1],[10,1]]))
data, (N, M) = img2mat( "plaatjes/smile.png" )
mat = FFT2D( data )
dict = mat2dict(mat)
mat_new = dict2mat(dict, N, M )
data_new = realintmat(iFFT2D( mat_new ))
for y in range(N):
  for x in range(M):
    pass
    #print data[y][x] - data_new[y][x]

#mat2img(realintmat( iFFT2D(mat_new) ), (N, M)).save("plaatjes/Usmile.jpg")
