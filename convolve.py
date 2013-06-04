import numpy as np

def downsampling_convolution( input, filter, step=2 ):
  F = len(filter)
  N = len(input)
  start = step - 1
  output = np.zeros( N )
  k = 0

  if F <= N:
    for i in range( start, F, step ):
      sum = 0
      for j in range( i ):
        sum += input[i-j]*filter[j]
      output[k] = sum
      k += 1
      start = i
    for i in range( start, N, step ):
      sum = input[i] * filter[0]
      for j in range( 1, F ):
        sum += input[i-j]*filter[j]
      output[k] = sum
      k += 1
      start = i
    for i in range( start, N+F-1, step ):
      sum = 0;
      for j in range( i-(N-1), F ):
        sum += input[i-j]*filter[j]
      output[k] = sum
      k += 1
  else:
    buffer = np.zeros( N + 2*(F-1) )
    buffer[F-1:1-F] = input
    stop = N + 2*(F-1)
    for i in range( start, stop, step ):
      sum = 0
      for j in range( F ):
        sum += buffer[i-j] * filter[j]
        output[k] = sum
        k += 1

  return output

def upsampling_convolution( input, filter, step=2 ):
  F = len(filter)
  N = len(input)
  k = (N-1) << 1
  output = np.zeros( 2*N ) #lengte moet nog even bepaald worden

  assert F >= 2

  for i in range( N-1, 0, -1 ):
    for j in range( F ):
      output[k] += input[i] * filter[j]
    k -= step
  return output

if __name__ == "__main__":
  a = np.array([0,1,2,3,4,5,6,0])
  b = np.array([1,-1])
  print downsampling_convolution( a, b )
  print upsampling_convolution( downsampling_convolution( a, b ), b )
