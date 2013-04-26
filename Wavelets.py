from math import sqrt, log
import numpy as np

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

class Wavelet( object ):
  _waveLength = None
  _dec_l = None
  _dec_h = None
  _rec_l = None
  _rec_h = None

  @classmethod
  def dwt( cls, input, steps = -1 ):
    if len( input.shape ) > 1:
      for i in input.shape:
        assert i == input.shape[0] #square/cube/etc

      #doe iets?
    else:
      n = len( input )
      output = input
      if steps < 0:
        steps = int(log( n, 2 ))

      for i in range( steps ):
        output = cls.next( output )

      return output
    

  @classmethod
  def idwt( cls, input, steps = -1 ):
    n = len( input )
    output = input
    print output
    if steps < 0:
      steps = int(log( n, 2 ))

    for i in range( steps ):
      output = cls.prev( output )

    return output

  @classmethod
  def next_2d( cls, input ):
    assert len(input.shape) == 2
    n, m = input.shape
    output = np.zeros(input.shape)

    for i in range(n): #rijen
      output[i,:] = cls.next( input[i,:] )

    for i in range(m): #kolommen
      output[:,i] = cls.next( input[:,i] )

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
        output[i]   = output[i]   + input[k] * cls._dec_l[j]
        output[i+h] = output[i+h] + input[k] * cls._dec_h[j]

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
        output[k] = output[k] + input[i]   * cls._rec_l[j]
        output[k] = output[k] + input[i+h] * cls._rec_h[j]

    return output

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
  """
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
