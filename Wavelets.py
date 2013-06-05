from math import sqrt, log
import numpy as np
import scipy.signal as signal
from FFT2util import minimaxpow2
from itertools import izip

"""
Goed. Even beetje uitleg: op wiki kan je zien hoe "One level of the transform"
werkt. Over het algemeen wil je even veel levels naar boven gaan als de 2-log
van de lengte van je input. Er wordt op elk niveau immers 1x downsampled met
factor 2.

Method `next' doet precies 1 niveau van de transformatie.
Method `dwt' doorloopt precies `steps' keer je `next' method.
Andersom dito.

Noot: dit is dus nog geen "fast" wavelet transform. -> OF TOCH WEL?
http://code.google.com/p/jwave/source/browse/trunk/src/main/java/math/transform/jwave/transforms/FastWaveletTransform.java?r=87
wat is die link in gods naam?
"""

def downsampling_convolution( input, filter ):
  F = len(filter)
  N = len(input)
  start = 1
  output = np.zeros( (N )//2 ) #(N - F - 1)//2
  k = 0

  #  print "N=",N
  #  if F <= N:
  #convolve het begin
  #    for i in range( start, F, 2):
  #  sum = 0
  #  for j in range( i+1 ):
  #    sum += input[i-j]*filter[j]
  #  output[k] = sum
  #  k += 1
  #  start = i + 2

  #convolve het midden
  for i in range( start, N, 2 ):
    sum = 0
    for j in range( F ):
      sum += input[i-j]*filter[j]
    output[k] = sum 
    k += 1
    start = i + 2

  #convolve het einde
  #for i in range( start, N+F-1, 2):
  #  sum = 0;
  #  for j in range( i-(N-1), F ):
  #    sum += input[i-j]*filter[j]
  #  output[k] = sum
  #  k += 1
  #  else:
  #    buffer = np.zeros( N + 2*(F-1) )
  #    buffer[F-1:1-F] = input
  #    start = F
  #    stop = N + 2*(F-1)
  #    for i in range( start, stop, 2 ):
  #      sum = 0
  #      for j in range( F ):
  #        sum += buffer[i-j] * filter[j]
  #        output[k] = sum
  #        k += 1
  #  print output
  return output

def upsampling_convolution( input, filter, step=2 ):
  F = len(filter)
  N = len(input)
  k = (N-1) << 1
  output = np.zeros( N ) #lengte moet nog even bepaald worden

  assert F >= 2

  for i in range( N-1, 0, -1 ):
    for j in range( F ):
      output[k] += input[i] * filter[j]
    k -= step
  return output

def upsampling_convolution_valid_sf( input, filter ):
  F = len( filter )
  N = len( input )
  output = np.zeros( 2 * N )
  # print N,F
  # assert F % 2 == 0 and N >= F//2

  filter_even = np.zeros( F//2 )
  filter_odd = np.zeros( F//2 )
  for i in range( F//2 ):
    filter_even[i] = filter[i << 1]
    filter_odd[i] = filter[(i << 1) + 1]

  k = F//2 - 1
  
  l = 0
  for i in range( N ):
    sum_even = 0
    sum_odd = 0 

    for j in range( F//2 ):
      sum_even += filter_even[j] * input[i-j]
      sum_odd += filter_odd[j] * input[i-j]
    #print sum_even, sum_odd, "sommie"
    output[l - 2*k] = sum_even
    l += 1
    output[l - 2*k] = sum_odd
    l += 1

  return output

def _is_pow2( num ):
  return num > 0 and ((num & (num - 1)) == 0)

class Wavelet( object ):
  _waveLength = None
  _dec_l = None
  _dec_h = None
  _rec_l = None
  _rec_h = None

  @classmethod
  def dwt( cls, input, steps = -1, tensor=False):
    if len( input.shape ) == 3:
      return cls.dwt3d(input,steps,tensor=tensor)
    elif len( input.shape ) == 2:
      return cls.dwt2d(input,steps,tensor=tensor)
    else:
      n = input.shape[0]
      output = np.copy( input )

      if n == 1:
        return output

      if not _is_pow2( n ):
        output = np.concatenate((output, [0 for i in range( minimaxpow2(n) - n)]))

      if steps < 0:
        steps = int(log(minimaxpow2(n), 2))

      print "we gaat %i steps doen" % steps

      for i in range( steps ):
        k = len(output)/(2**i)
        output[0:k] = cls.next(output[0:k])

      return output

  @classmethod
  def idwt( cls, input, steps = -1, m = -1, tensor=False ):
    if m == -1:
      m = input.shape[0]
    if len( input.shape ) == 3:
      return cls.idwt3d(input,steps,m,tensor=tensor)
    elif len( input.shape ) == 2:
      return cls.idwt2d(input,steps,m,tensor=tensor)
    else:
      n = len( input )
      output = input.copy()

      if n == 1:
        return output

      if not _is_pow2( n ):
        output = np.concatenate((output, [0 for i in range( minimaxpow2(n) - n)]))

      if steps < 0:
        steps = int(log(minimaxpow2(n), 2))

      print "we gaan %i steps terug doen zwa" % steps

      for i in range( steps ):
        j = steps - i-1
        k = len(output)/(2**j)
        output[0:k] = cls.prev(output[0:k])
        #print "vorige rondeeee"

      return output[0:m]

  @classmethod
  def dwt2d( cls, input, steps = -1, tensor=False ):
    assert len(input.shape) == 2
    n = input.shape[0]
    for i in input.shape:
      assert _is_pow2(i) #alleen machten van 2 so far
      
    output = np.copy( input )
  
    if n == 1:
      return output

    if steps < 0:
      steps = int( log( minimaxpow2(n), 2))
      
    print "we gaan %i steps doen" % steps

    if not tensor:
      for i in range( steps ):
        k = len( output )/(2**i)
        output[0:k,0:k] = cls.next_2d( output[0:k,0:k] )
        #print "volgende rondee:)"
    else:
      for i in range( steps ):
        k = len(output ) / (2**i)
        for p in range(n):
          output[p,0:k] = cls.next( output[p,0:k] )
        for p in range(n):
          output[0:k,p] = cls.next( output[0:k,p] )
    return output

  @classmethod
  def idwt2d( cls, input, steps = -1, m = -1, tensor=False ):
    assert len(input.shape) == 2
    n = input.shape[0]
    assert _is_pow2(n) #alleen machten van 2 so far
    for i in input.shape:
      assert i == n #square/cube/etc

    output = np.copy( input )

    if m<0:
      m = n

    if n == 1:
      return output

    if steps < 0:
      steps = int(log(minimaxpow2(n), 2))

    print "we gaan %i steps terugdoen" % steps

    if not tensor:
      for i in range( steps ):
        j = steps - i - 1
        k = len(output ) / (2**j)
        output[0:k,0:k] = cls.prev_2d( output[0:k,0:k] )
        #print "vorige ronde!"
    else:
      for i in range( steps ):
        j = steps - i - 1
        k = len(output ) / (2**j)
        for p in range(n):
          output[0:k,p] = cls.prev( output[0:k,p] )
        for p in range(n):
          output[p,0:k] = cls.prev( output[p,0:k] )
      
    return output[0:m,0:m]

  @classmethod
  def dwt3d( cls, input, steps = -1, tensor = False ):
    assert len(input.shape) == 3
    for i in input.shape:
      assert _is_pow2(i)

    n = input.shape[0]
    output = np.copy( input )

    if n == 1:
      return output

    if steps < 0:
      steps = int( log( minimaxpow2(n), 2) )

    if not tensor:
      for i in range( steps ):
        print "nieuwe ronde %i van %i!" % (i, steps)
        k = len( output ) / ( 2 ** i )
        output[ 0:k, 0:k, 0:k ] = cls.next_3d( output[ 0:k, 0:k, 0:k ] )
    else:
      for i in range( steps ):
        k = len( output ) / (2**i)
        for p in range( n ):
          output[p,0:k,0:k] = cls.next_2d( output[p, 0:k, 0:k] )
        for p in range( n ):
          for q in range( n ):
            output[0:k,p,q] = cls.next( output[0:k,p,q] )

        
    return output

  @classmethod
  def idwt3d( cls, input, steps = -1, m = -1, tensor=False ):
    assert len(input.shape) == 3

    n = input.shape[0]
    output = np.copy( input )

    if n == 1:
      return output 

    if m < 0:
      m = n
  
    if steps < 0:
      steps = int( log( minimaxpow2(n), 2) )

    if not tensor:
      for i in range( steps ):
        j = steps - i - 1
        k = len( output ) / ( 2 ** j )
        output[ 0:k, 0:k, 0:k ] = cls.prev_3d( output[ 0:k, 0:k, 0:k ] )
    else:
      for i in range( steps ):
        j = steps - i - 1
        k = len( output ) / ( 2 ** j )
        for p in range( n ):
          for q in range( n ):
            output[0:k,p,q] = cls.prev( output[0:k,p,q] )
        for p in range( n ):
          output[p,0:k,0:k] = cls.prev_2d( output[p, 0:k, 0:k] )

    return output[ 0:m, 0:m, 0:m ]

  """
  Voor 2d zie https://github.com/nigma/pywt/blob/master/src/pywt/multidim.py
  en http://code.google.com/p/jwave/source/browse/trunk/src/main/java/math/jwave/transforms/FastWaveletTransform.java

  Voor unit tests van jwave zie
  http://code.google.com/p/jwave/source/browse/trunk/src/test/java/math/jwave/transforms/FastWaveletTransformTest.java
  en die van pywt kan men gewoon zelf doen (door pywt te installen)

  Het lijkt er op dat jwave iets anders doet dan pywt maar is me niet helemaal duidelijk.
  """

  @classmethod
  def next_2d( cls, input ):
    assert len(input.shape) == 2 #alleen vierkanten
    x, y = input.shape
    assert _is_pow2(x) and _is_pow2(y)
    output = np.copy( input )

    for j in range(x): #rows
      output[j,:] = cls.next( output[j,:] )

    for i in range(y): #cols
      output[:,i] = cls.next( output[:,i] )

    return output

  @classmethod
  def prev_2d( cls, input ):
    assert len( input.shape ) == 2
    x, y = input.shape
    output = np.copy( input )

    for j in range(x): #rows
      output[j,:] = cls.prev( output[j,:] )

    for i in range(y): #cols
      output[:,i] = cls.prev( output[:,i] )

    return output

  @classmethod
  def next_3d( cls, input ):
    assert len( input.shape ) == 3
    x, y, z = input.shape
    assert _is_pow2(x) and _is_pow2(y) and _is_pow2(z)
    output = np.copy( input )

    for i in range(x): #rows
      output[i,:,:] = cls.next_2d( output[i,:,:] )

    for j in range(y): #..layers? slices? stacks? fibers? dunno, pick a word.
      for k in range(z):
        output[:,j,k] = cls.next( output[:,j,k] )

    return output

  @classmethod
  def prev_3d( cls, input ):
    assert len( input.shape ) == 3
    x, y, z = input.shape
    output = np.copy( input )

    for i in range(x): #rows
      output[i,:,:] = cls.prev_2d( output[i,:,:] )

    for j in range(y): #..layers? slices? stacks? fibers? dunno, pick a word.
      for k in range(z):
        output[:,j,k] = cls.prev( output[:,j,k] )

    return output

  """
  Doet een 1d stapje vooruit. Zie http://code.google.com/p/jwave
  """
  @classmethod
  def next( cls, input ):
    assert len(input.shape) == 1 and _is_pow2( len(input) )

    low = downsampling_convolution( input, cls._dec_l )
    hi = downsampling_convolution( input, cls._dec_h )

    return np.concatenate( (low, hi) )

  """
  Doet een 1d stapje terug.
  """
  @classmethod
  def prev( cls, input ):
    assert len(input.shape) == 1 and _is_pow2( len(input) )
    N = len(input)

    output = upsampling_convolution_valid_sf( input[:N//2], cls._rec_l ) +  \
        upsampling_convolution_valid_sf( input[N//2:], cls._rec_h )
    #print input, output
    return output

#zie http://faculty.gvsu.edu/aboufade/web/wavelets/student_work/EF/how-works.html
class BiOrtho97Wavelet( Wavelet ):
  _waveLength = 9
  _dec_l = np.array([
    0.02674875741080976,
    -0.01686411844287495,
    -0.07822326652898785,
    0.2668641184428723,
    0.6029490182363579,
    0.2668641184428723,
    -0.07822326652898785,
    -0.01686411844287495,
    0.02674875741080976
  ]) * sqrt(2)
  _dec_h = np.array([
    0.0,
    0.09127176311424948,
    -0.05754352622849957,
    -0.5912717631142470,
    1.115087052456994,
    -0.5912717631142470,
    -0.05754352622849957,
    0.09127176311424948,
    0.0
  ]) * sqrt(2)
  _rec_l = np.array([
    0.0,
    -0.09127176311424948,
    -0.05754352622849957,
    0.5912717631142470,
    1.115087052456994,
    0.5912717631142470,
    -0.05754352622849957,
    -0.09127176311424948,
    0.0
  ]) * sqrt(2)
  _rec_h = np.array([
    0.02674875741080976,
    0.01686411844287495,
    -0.07822326652898785,
    -0.2668641184428723,
    0.6029490182363579,
    -0.2668641184428723,
    -0.07822326652898785,
    0.01686411844287495,
    0.02674875741080976
  ]) * sqrt(2)

class BiOrtho53Wavelet( Wavelet ):
  _waveLength = 5
  _dec_l = np.array([
    -1.0/8,
    2.0/8,
    6.0/8,
    2.0/8,
    -1.0/8
  ]) * sqrt(2)
  _dec_h = np.array([
    0.0,
    -1.0/2,
    1.0,
    -1.0/2,
    0.0
  ]) * sqrt(2)
  _rec_l = np.array([
    -0.0,
    -1.0/2,
    -1.0,
    -1.0/2,
    -0.0
  ]) * sqrt(2)
  _rec_h = np.array([
    -1.0/8,
    -2.0/8,
    6.0/8,
    -2.0/8,
    -1.0/8
  ]) * sqrt(2)

class Daubechies2Wavelet( Wavelet ):
  _waveLength = 4
  _dec_l = np.array([
    -0.12940952255092145,
    0.22414386804185735,
    0.83651630373746899,
    0.48296291314469025
  ])
  _dec_h = np.array([
    -0.48296291314469025,
    0.83651630373746899,
    -0.22414386804185735,
    -0.12940952255092145
  ])
  _rec_l = np.array([
    0.48296291314469025,
    0.83651630373746899,
    0.22414386804185735,
    -0.12940952255092145
  ])
  _rec_h = np.array([
    -0.12940952255092145,
    -0.22414386804185735,
    0.83651630373746899,
    -0.48296291314469025
  ])

class HaarWavelet( Wavelet ):
  # zie http://wavelets.pybytes.com/wavelet/haar/
  _waveLength = 2
  _dec_l = np.array([   1.,  1.])/sqrt(2.0)
  _dec_h = np.array([   -1., 1.])/sqrt(2.0)
  _rec_l = np.array([   1.,  1.])/sqrt(2.0)
  _rec_h = np.array([   1.,  -1.])/sqrt(2.0)
  
  """
  dit is de versie zoals hij op wiki staat. Boven is de algemenere versie,
  hoewel ik dat nog niet getest heb met andere wavelets.

  @classmethod
  def next( cls, input ):
    assert len(input.shape) == 1
    n = len(input)
    output = np.zeros(n)
    h = n >> 1

    for i in range(h):
      #neem de som (genormaliseerd)
      output[i]   = output[i]   + input[2*i]   * cls._dec_l[0] \
                                + input[2*i+1] * cls._dec_l[1]
      #neem het verschil (genormaliseerd)
      output[i+h] = output[i+h] + input[2*i]   * cls._dec_h[0] \
                                + input[2*i+1] * cls._dec_h[1]


    return output

  @classmethod
  def prev( cls, input ):
    assert len(input.shape) == 1
    n = len( input )
    output = np.zeros(n)
    h = n >> 1

    for i in range(h):
      output[2*i]   = output[2*i]   + input[i]   * cls._rec_l[0] \
                                    + input[i+h] * cls._rec_l[1]
      output[2*i+1] = output[2*i+1] + input[i]   * cls._rec_h[0] \
                                    + input[i+h] * cls._rec_h[1]

    return output
  """
