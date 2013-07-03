from Wavelet_Defs import wavelet_dict
from Tools import find_cutoff_nd

from channels import *
from sys import argv
from FFT2util import FFT2D,iFFT2D,matslice,realintmat
from FFTjan import mat2dict,dict2mat
import pywt
import numpy as np
from math import sqrt,copysign
from threshold import *

def mat5dict( mat, cutoff, threshfunc ):
  N,M = (len(mat),len(mat[0]))
  dict = {}
  for y in range(N):
    for x in range(M):
      try:
        thresh = threshfunc(mat[y][x],cutoff)
        dict[y*M + x] = thresh #mat[y][x]
      except:
        pass
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
      tuplist += [tuple([int(mat[y,x]) for mat in data])]
  
  #print len(tuplist),len(tuplist[0])

  img = Image.new('RGBA'[:len(tuplist)],(size[1],size[0]))
  img.putdata(tuplist)
  return img

def find_cutoff( ar, ratio ):
  if ratio > 1 or ratio < 0:
    print "fuck off biatch",ratio
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

def main(infile):
  global mycompress,mywavelet,myoutfile,mytensor,mythreshfunc

  data, dim = img3mat(infile)
  
  data = map(lambda x: np.array(x), data)
  data_float = map(lambda x: x.astype('float'),data)

  print "Starting encoding of image %s" % (argv[1])
  print "TensorProduct =",mytensor
  print "Threshold func =",mythreshfunc
  print "Image has dimensions : %i,%i" % dim
  print

  encoded = map(lambda x: mywavelet.dwt(x,tensor=mytensor),data_float)
  interdims = (len(encoded[0]),len(encoded[0][0]))

  print "Encoding done"
  #  print_dimensions_matlist("Encoded dims:",encoded)
  print "Using dimensions:",interdims
  print

  """ Temporary bypass to check for problems in main algorithm -- Confirmed """
  cutoff = find_cutoff_nd( encoded, mycompress )
  
  print "Converted to dictionaries:"
  print "Compression cutoff is %f" % cutoff

  dicks = map(lambda x: mat5dict(x,cutoff,mythreshfunc),encoded)

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

  decoded = map(lambda x: mywavelet.idwt(x,tensor=mytensor),lists)

  print "Decoding done"  
  #  print_dimensions_matlist("Decoded dimensions are:",decoded)
  #  print

  sliced = map(lambda x: np.rint(x).astype(data[0].dtype),decoded)

  #  print_dimensions_matlist("Sliced dimensions are:",sliced)

  if myoutfile == None:
    filename = infile.replace('.','_new.')
  else:
    filename = myoutfile
  print "Saving to",filename
  mat5img(sliced,dim).save(filename)
  
if __name__ == "__main__":
  # Dit stuk regelt de CLI options
  from sys import stderr
  import CLI,sys
  my_opts = [
    # short, long, args, description
    ('t','tensor',0,"turn on tensor mode"),
    ('s','smooth',0,"activate quadratic threshold"),
    ('l','logsmooth',0,"activate logarithmic theshold"),
    ('w','wavelet',1,"select wavelet <arg>"),
    ('c','compress',1,"set compression to <arg>"),
    ('o','output',1,"set destination to <arg>"),
    ('h','help',0,'print this message')
  ]
  my_usage = CLI.usage("python wave_img.py [picture] [options]",
                       "Uses various wavelets to compress and then decompress a picture",
                       my_opts)
  try:
    args, opts = CLI.parse_args(sys.argv,my_opts) #throws IOError on error
  except IOError:
    print my_usage.short()
    exit(1)

  #set defaults for various options
  from Wavelet_Defs import wavelet_dict
  mywavelet = wavelet_dict['haar']
  mycompress = 1.0
  myoutfile = None
  mytensor = False
  mythreshfunc = threshold_hard

  for o in opts:
    if o[0] == 'wavelet':
      try:
        mywavelet = wavelet_dict[o[1]]
      except:
        print >>stderr,o[1],'is not a valid wavelet'
        exit(1)
    elif o[0] == 'compress':
      try:
        mycompress = float(o[1]) 
      except TypeError:
        exit(1)
    elif o[0] == 'output':
      myoutfile = o[1]
    elif o[0] == 'tensor':
      mytensor = True
    elif o[0] == 'help':
      print my_usage
      exit(1)
    elif o[0] == 'smooth':
      mythreshfunc = threshold_quad
    elif o[0] == 'logsmooth':
      mythreshfunc = threshold_log

  if len(args) == 1: # additional IOError
    print my_usage.short()
    exit(1)
  
  map(main,args[1:])

