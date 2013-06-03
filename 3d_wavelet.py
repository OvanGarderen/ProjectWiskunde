import numpy as np
from Wavelets import *
from driedeeding import mat_3d_to_dict, dict_to_mat_3d
from Tools import find_cutoff_nd
from PSNR import PSNR
import Image,ImageSequence
import images2gif as gifs

def read7Gif( fn ):
  im = Image.open(fn)
  print im.info
  frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
  return frames

def plaatje():
  frames = read7Gif( "plaatjes/croppedgif.gif" )
  i=0
  for f in frames:
    f.save("gif/frame%i.png" % i)
    i+=1
  gifs.writeGif( "gif/lel_new.gif", frames)

def main():
  x = np.array(
    [[[1,1,1,1],
      [1,1,1,1],
      [1,1,0,1],
      [1,1,1,1]],
     [[1,1,1,1],
      [1,1,1,1],
      [1,1,1,1],
      [1,1,1,1]],
     [[1,1,1,1],
      [1,1,1,1],
      [1,1,2,1],
      [1,1,1,1]],
     [[1,1,1,1],
      [1,1,1,1],
      [1,1,3,1],
      [1,1,1,1]]]
  )
  x_float = x.astype('float')

  wavelet = HaarWavelet

  X = wavelet.dwt(x_float)
  cutoff = find_cutoff_nd( X, 0.3 )

  print X
  print cutoff

  dict = mat_3d_to_dict( X, cutoff )
  X_ = dict_to_mat_3d( dict, X.shape[0], X.shape[1], X.shape[2] )

  print dict

  x_ = wavelet.idwt(X_)
  print x_
  print PSNR( x_float, x_ )

if __name__ == "__main__":
  plaatje()
