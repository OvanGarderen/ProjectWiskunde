from math import sqrt, log
import numpy as np
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

def _is_pow2( num ):
  return num > 0 and ((num & (num - 1)) == 0)

class Wavelet( object ):
  _waveLength = None
  _dec_l = None
  _dec_h = None
  _rec_l = None
  _rec_h = None

  @classmethod
  def dwt( cls, input, steps = -1 ):
    print np.sum(cls._dec_l)
    output = input.copy()
    if len( input.shape ) == 2:
      return cls.dwt2d(output,steps)
    else:
      n = len( input )

      if n == 1:
        return output

      if not _is_pow2( n ):
        output = np.concatenate((output, [0 for i in range( minimaxpow2(n) - n)]))

      if steps < 0:
        steps = int(log(minimaxpow2(n), 2))

      print "we gaat %i steps doen" % steps

      for i in range( steps ):
        #output = np.concatenate((cls.next( output[0: len(output)/(2**i)] ), output[len(output)/2**i:]))
        k = len(output)/(2**i)
        output[0:k] = cls.next(output[0:k])
        #print "volgende rondeeee:)"

      return output

  @classmethod
  def idwt( cls, input, steps = -1, m = -1 ):
    output = input.copy()
    if m == -1:
      m = input.shape[0]
    if len( input.shape ) == 2:
      return cls.idwt2d(output,steps,m)
    else:
      n = input.shape[0]

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
        print "vorige rondeeee"

      return output[0:m]

  @classmethod
  def dwt2d( cls, input, steps = -1 ):
    n = input.shape[0]
    assert _is_pow2(n) #alleen machten van 2 so far
    for i in input.shape:
      assert i == n #square/cube/etc
      
    output = input
  
    if n == 1:
      return output

    if steps < 0:
      steps = int( log( minimaxpow2(n), 2))
      
    print "we gaan %i steps doen" % steps

    for i in range( steps ):
      k = len( output )/(2**i)
      output[0:k,0:k] = cls.next_2d( output[0:k,0:k] )
      #print "volgende rondee:)"

    return output

  @classmethod
  def idwt2d( cls, input, steps = -1, m = -1 ):
    n = input.shape[0]
    assert _is_pow2(n) #alleen machten van 2 so far
    for i in input.shape:
      assert i == n #square/cube/etc

    output = input

    if m<0:
      m = n

    if n == 1:
      return output

    if steps < 0:
      steps = int(log(minimaxpow2(n), 2))

    print "we gaan %i steps terugdoen" % steps

    for i in range( steps ):
      j = steps - i - 1
      k = len(output ) / (2**j)
      output[0:k,0:k] = cls.prev_2d( output[0:k,0:k] )
      #print "vorige ronde!"

    return output[0:m,0:m]


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
    n, m = input.shape #rijen, kolommen
    assert _is_pow2(n)
    output = np.zeros(input.shape) #init matrix

    H = np.zeros( (m,n/2) )
    L = np.zeros( (m,n/2) )
    for i in range(m):
      out = cls.next( input[i,:] )
      L[i] = out[:n/2]
      H[i] = out[n/2:]

    H = np.transpose(H)
    L = np.transpose(L)

    LL, LH = np.zeros( (m/2,n/2) ), np.zeros( (m/2,n/2) )
    for i in range(m/2):
      out = cls.next( L[i] )
      LL[i] = out[:n/2]
      LH[i] = out[n/2:]
    del L

    HL, HH = np.zeros( (m/2,n/2) ), np.zeros( (m/2,n/2) )
    for i in range(m/2):
      out = cls.next( H[i] )
      HL[i] = out[:n/2]
      HH[i] = out[n/2:]
    del H

    output[:n/2,:n/2] = np.transpose(LL)
    output[:n/2,n/2:] = np.transpose(LH)
    output[n/2:,:n/2] = np.transpose(HL)
    output[n/2:,n/2:] = np.transpose(HH)

    return output

  @classmethod
  def prev_2d( cls, input ):
    assert len( input.shape ) == 2
    n, m = input.shape
    assert _is_pow2(n)
    output = np.zeros( input.shape )

    LL = np.transpose( input[:n/2,:n/2] )
    LH = np.transpose( input[:n/2,n/2:] )
    HL = np.transpose( input[n/2:,:n/2] )
    HH = np.transpose( input[n/2:,n/2:] )

    L = np.zeros( (n/2, n) )
    i = 0
    for rowL, rowH in izip( LL, LH ):
      L[i,:] = cls.prev( np.concatenate( (rowL, rowH) ) )
      i += 1
    del LL, LH

    H = np.zeros( (n/2, n) )
    i = 0
    for rowL, rowH in izip( HL, HH ):
      H[i,:] = cls.prev( np.concatenate( (rowL, rowH) ) )
      i += 1
    del HL, HH

    L = np.transpose( L )
    H = np.transpose( H )

    i = 0
    for rowL, rowH in izip( L, H ):
      output[i,:] = cls.prev( np.concatenate( (rowL, rowH) ) )
      i += 1

    return output

  """
  @classmethod
  def next_2d( cls, input ):
    assert len(input.shape) == 2 #alleen vierkanten
    n, m = input.shape
    assert _is_pow2(n) and _is_pow2(m)
    output = np.zeros(input.shape) #init matrix

    for i in range(m): #rijen
      output[i,:] = cls.next( input[i,:] )

    for j in range(n): #kolommen
      output[:,j] = cls.next( input[:,j] )

    return output

  @classmethod
  def prev_2d( cls, input ):
    assert len( input.shape ) == 2
    n, m = input.shape
    output = np.zeros( input.shape )

    for i in range(m): #kolommen
      output[:,i] = cls.prev( input[:,i] )

    for i in range(n): #rijen
      output[i,:] = cls.prev( input[i,:] )

    return output
  """

  """
  Doet een 1d stapje vooruit. Zie http://code.google.com/p/jwave
  """
  @classmethod
  def next( cls, input ):
    assert len(input.shape) == 1
    n = len(input)
    output = np.zeros(n)
    k = 0
    h = n >> 1

    for i in range(h):
      for j in range(cls._waveLength):
        k = ( (i << 1) + j ) % n
        output[i]   += input[k] * cls._dec_l[j]
        output[i+h] += input[k] * cls._dec_h[j]

    return output

  """
  Doet een 1d stapje terug.
  """
  @classmethod
  def prev( cls, input ):
    assert len(input.shape) == 1
    n = len( input )
    output = np.zeros(n)
    k = 0
    h = n >> 1

    for i in range(h):
      for j in range( cls._waveLength ):
        k = ( (i << 1) + j ) % n
        output[k] += input[i]   * cls._rec_l[j]  \
                   + input[i+h] * cls._rec_h[j]

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
    0.0,
    1.0/2,
    1.0,
    1.0/2,
    0.0
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
  _dec_l = np.array([  1,  1])/sqrt(2.0)
  _dec_h = np.array([ -1,  1])/sqrt(2.0)
  _rec_l = np.array([  1,  1])/sqrt(2.0)
  _rec_h = np.array([  1, -1])/sqrt(2.0)
  
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
