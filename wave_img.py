from Wavelets import HaarWavelet
from channels import *
from sys import argv
from FFT2util import FFT2D,iFFT2D,matslice,realintmat
from FFTjan import mat2dict,dict2mat
import pywt
import numpy as np
from math import sqrt

def mat5dict( mat, cutoff ):
  N,M = (len(mat),len(mat[0]))
  dict = {}
  for y in range(N):
    for x in range(M):
      if abs(mat[y][x]) >= cutoff:
        dict[y*M + x] = mat[y][x]
  return dict

def dict5mat( dict, N, M ):
  mat = np.zeros((M,N))
  for y in range(N):
    for x in range(M):
      i = y*M + x
      mat[y,x] = dict[i] if i in dict else 0.0
  return mat

def mat5img( data, size ):
  tuplist = []
  for y in xrange(len(data[0])):
    for x in xrange(len(data[0][0])):
      tuplist += [tuple([mat[y,x] for mat in data])]
  
  print len(tuplist),len(tuplist[0])

  img = Image.new('RGBA'[:len(tuplist)],(size[1],size[0]))
  img.putdata(tuplist)
  return img

def find_cutoff( ar, ratio ):
  if ratio > 1 or ratio < 0:
    print "fuck off biatch"
    assert 0

  a = np.sort(np.absolute(ar))
  return a[int((1-ratio)*len(ar))]

def print_dimensions_matlist(stri, matlist):
  print stri
  for x in matlist:
    print len(x),len(x[0])

"""
def testje():
  print "Begin testje"
  
  a = np.array([[1,2,3,4],
                [0,8,6,4],
                [2,3,5,7],
                [11,13,17,19]]).astype('float')
  print a
  b = HaarWavelet.dwt(a)
  print np.rint(b)
  c = HaarWavelet.idwt(b)
  print np.rint(c)
"""

def main():
  data, dim = img3mat(argv[1])
  
  data = map(lambda x: np.array(x), data)
  data_float = map(lambda x: x.astype('float'),data)

  print "Starting encoding of image %s" % (argv[1])
  print "Image has dimensions : %i,%i" % dim
  print

  encoded = map(HaarWavelet.dwt,data_float)
  interdims = (len(encoded[0]),len(encoded[0][0]))

  print "Encoding done"
#  print_dimensions_matlist("Encoded dims:",encoded)
  print "Using dimensions:",interdims
  print

  """ Temporary bypass to check for problems in main algorithm -- Confirmed """
  compression = 40.5

  print "Converted to dictionaries:"
  print "Compression cutoff is %f" % compression

  dicks = map(lambda x: mat5dict(x,compression),encoded)

  print "Dictionary lengths:"
  for x in dicks:
    print len(x)

  print "Compression factor per channel:"
  print map(lambda x: compress(x[0],x[1]), zip(dicks,encoded))
  print

  print "Converting dictionaries to matrices"
  print "Dimensions are %i,%i" % interdims

  lists = map(lambda x: dict5mat(x,interdims[0],interdims[1]),dicks)  
  lists = map(lambda x: np.array(x), lists)

  print "Starting decoding"

  decoded = map(HaarWavelet.idwt,lists)

  print "Decoding done"  
  #  print_dimensions_matlist("Decoded dimensions are:",decoded)
  #  print

  sliced = map(lambda x: np.rint(x).astype(data[0].dtype),decoded)

  #  print_dimensions_matlist("Sliced dimensions are:",sliced)

  filename = argv[1].replace('.','_new.')
  print "Saving to",filename
  mat5img(sliced,dim).save(filename)
  
if __name__ == "__main__":
#  testje()
  main()
