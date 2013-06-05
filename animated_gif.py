from subprocess import call
from PSNR import PSNR
from glob import glob
import os
from channels import *
import numpy as np
from Tools import find_cutoff_nd
from Wavelet_Defs import wavelet_dict
from driedeeding import mat_3d_to_dict, dict_to_mat_3d
from wave_img import mat5img

wave = wavelet_dict['db2']

def plaatje(plaat):
  print "splitting up gif... (this may take a while)"
  call(["gifsicle", "--unoptimize", "-e", plaat, "-o", plaat])

  gifs = sorted(glob(''.join([plaat,".*"])))
  driedlist = [[],[],[],[]]

  for f in gifs:
    data, dim = img3mat( f )
    for i in range( len(data) ):
      driedlist[i].append(data[i])

  data = map( lambda x: np.array( x ), driedlist )
  print np.array(data).shape
  data_float = map( lambda x: x.astype('float'), data )

  encoded = np.array(map( lambda x: wave.dwt(x,tensor=True), data_float ))
  interdims = encoded[0].shape
  print "interdims:", interdims

  compression = find_cutoff_nd( encoded, 0.01 )

  dicks = map( lambda x: mat_3d_to_dict( x, compression ), encoded )
  print map( lambda x: compress( x[0], x[1] ), zip( dicks, encoded ) )

  lists = map( lambda x: dict_to_mat_3d( x, interdims[0], interdims[1], interdims[2]), dicks )
  lists = map( lambda x: np.array(x), lists )

  decoded = map( lambda x: wave.idwt(x,tensor=True), lists )
  sliced = map( lambda x: np.rint(x).astype( data[0].dtype ), decoded )
  print PSNR( np.array(data), np.array(sliced) )

  frames, rows, cols = sliced[0].shape
  channels = len(sliced)
  frame_list = [] #np.zeros((frames, rows, cols, channels))
  #maak van lijst van channels, een lijst van frames
  for i in range( frames ):
    frame = np.zeros((channels, rows, cols))
    for j in range( channels ):
      frame[j,:,:] = sliced[j][i,:,:]
    frame_list.append(frame)

  print "converting gifs"
  for i, frame in enumerate( frame_list ):
    print "converting frame %i" % i
    fn = ''.join(["gif/temp.", str(i).zfill(3), ".png"])
    mat5img(frame, (rows, cols) ).save( fn )
    os.system(' '.join(["convert", fn, fn.replace("png", "gif")]))

  print "creating gif"
  os.system(''.join(["gifsicle -d 10 --loopcount=forever -m ","gif/temp.*.gif"," > ",plaat.replace(".", "_new.")]))

  print "removing temp files"
  call(["rm"]+list(glob('gif/temp.*.gif')))
  call(["rm"]+list(glob('gif/temp.*.png')))

if __name__ == "__main__":
  plaatje("gif/croppedgif.gif")
