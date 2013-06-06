from math import sqrt,copysign

def threshold_quad( coef, cutoff):
  if abs(coef) > cutoff:
    return copysign(
      sqrt( coef**2 - cutoff**2 ),coef)
  raise Exception

def threshold_log( coef, cutoff):
  if abs(coef) > cutoff:
    return copysign(
      log( exp(coef) - exp(cutoff) ),coef)
  raise Exception

def threshold_hard( coef, cutoff):
  if abs(coef) > cutoff:
    return coef
  raise Exception
