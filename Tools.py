def find_cutoff_nd( array ):
  if ratio < 0 or ratio > 1: assert 0
  output = np.reshape(array, reduce(lambda x, y: x * y, array.shape)) #reshape naar 1 lang ding
  return output[(1-ratio)*len(output)]
