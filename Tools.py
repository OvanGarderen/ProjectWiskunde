import numpy as np

def find_cutoff_nd( array, ratio ):
  if ratio < 0 or ratio > 1: assert 0
  if ratio == 0: return 0.0
  output = np.copy(array)
  output = np.reshape(output, reduce(lambda x, y: x * y, output.shape)) #reshape naar 1 lang ding
  output = np.sort( np.absolute( output ) )
  return output[int((1-ratio)*len(output))]
