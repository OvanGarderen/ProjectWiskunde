from PIL import Image
from channels import listtomat, compress
from Wavelets import HaarWavelet as haar
import images2gif as gifs
from Tools import find_cutoff_nd

import numpy as np
import sys

def mat_3d_to_dict( mat, cutoff ):
  K, L, M = (len(mat), len(mat[0]), len(mat[0][0]))
  dict = {}
  for z in range( M ):
    for y in range( L ):
      for x in range( K ):
        if abs( mat[z,y,x] ) > cutoff:
          dict[ z*K*L + y*K + x ] = mat[z,y,x]
  return dict

def dict_to_mat_3d( dict, K, L, M ):
  mat = np.zeros( (K, L, M) )
  for z in range( M ):
    for y in range( L ):
      for x in range( K ):
        i = z*K*L + y*K + x
        mat[z,y,x] = dict[i] if i in dict else 0.0
  return mat

def processImage(infile):
    driedlist = [[],[],[],[]]

    frames = gifs.readGif(infile,True)
    for frame in frames:
      for i in range( frame.shape[2] ):
        driedlist[i].append(frame[:,:,i])

#    print "chan, frames, height, width:\n",len(driedlist),len(driedlist[0]),len(driedlist[0][0]),len(driedlist[0][0][0])
    return (driedlist, len( driedlist[0] ), (len(driedlist[0][0]), len(driedlist[0][0][0])))

if __name__ == "__main__":
    name = sys.argv[1]
    data, frames, dim = processImage(name)
    #print data, frames, dim
    mywavelet = haar
  
    data = map(lambda x: np.array(x), data)
    data_float = map(lambda x: x.astype('float'),data)

    print "Starting encoding of image %s" % (sys.argv[1])
    print "Image has dimensions : %i,%i" % dim
    print

    encoded = map(mywavelet.dwt,data_float)
    interdims = encoded[0].shape

    print "Encoding done"
    print "Using dimensions:",interdims
    print

    # Temporary bypass to check for problems in main algorithm -- Confirmed 
    compression = find_cutoff_nd( encoded, 0.0 )

    print "Converted to dictionaries:"
    print "Compression cutoff is %f" % compression

    dicks = map(lambda x: mat_3d_to_dict(x,compression),encoded)

    print "Dictionary lengths:"
    for x in dicks: 
      print len(x)

    print "Compression factor per channel:"
    print map(lambda x: compress(x[0],x[1]), zip(dicks,encoded))
    print

    print "Converting dictionaries to matrices"
    print "Dimensions are %i,%i,%i" % interdims

    lists = map(lambda x: dict_to_mat_3d(x,interdims[0],interdims[1], interdims[2]),dicks)  
    lists = map(lambda x: np.array(x), lists)
    print "Starting decoding"

    decoded = map(mywavelet.idwt,encoded)

    print "Decoding done"  

    sliced = map(lambda x: np.rint(x).astype(data[0].dtype),decoded)

    frames, rows, cols = sliced[0].shape
    channels = len(sliced)
    frame_list = [] #np.zeros((frames, rows, cols, channels))
    #maak van lijst van channels, een lijst van frames
    for i in range( frames ):
      frame = np.zeros((rows, cols, channels))
      for j in range( channels ):
        frame[:,:,j] = sliced[j][i,:,:]
      frame_list.append(frame)

    #  print_dimensions_matlist("Sliced dimensions are:",sliced)

    filename = sys.argv[1].replace('.','_new.')
    print "Saving to",filename
    gifs.writeGif( filename, frame_list )
