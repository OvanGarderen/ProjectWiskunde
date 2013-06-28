#Peak signal to noise ratio implementatie. zie wikipedia
import numpy as np
from channels import *
from sys import argv
from math import log

def PSNR( s1, s2 ):
  assert s1.shape == s2.shape
  factor = np.prod( [s1.shape, s2.shape] )
  sum_squared = np.sum(np.square(s1-s2))
  maximal_value = np.amax( np.array((s1, s2)) )
  if sum_squared == 0: return np.inf
  psnr = 20 * log(maximal_value, 10) - 10*log(sum_squared, 10)
  return psnr

def do_PSNR(ls):
  ref = np.array(img3mat(ls[1])[0])
  imges = zip( map(lambda x: PSNR( ref, np.array(img3mat(x)[0]) ), ls[2:] ), ls[2:] )
  return imges

if __name__ == "__main__":
  if len(ls) > 2:
    imges = do_PSNR(argv)
    for i in range(len( imges )):
        print "psnr for %s: %f" % (imges[i][1], imges[i][0] )
    
