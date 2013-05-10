#Peak signal to noise ratio implementatie. zie wikipedia
import numpy as np
from math import log

def PSNR( s1, s2, is_float = False):
  assert s1.shape == s2.shape
  factor = np.prod( [s1.shape, s2.shape] )
  sum_squared = np.sum(np.square(s1-s2))
  maximal_value = np.finfo( s1.dtype ).max if is_float else np.iinfo(s1.dtype).max
  if sum_squared == 0: return np.inf
  psnr = 20 * log(maximal_value, 10) - 10*log(sum_squared, 10)
  return psnr
