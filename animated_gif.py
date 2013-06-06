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
from threshold import *

def plaatje(plaat):
  global mywavelet, mycompress, myoutfile, mytensor, mydelay, mytensor, mythreshfunc

  print "compressing",plaat
  print "tensor is %s" % ("on" if mytensor else "off")
  print "thresholding :",mythreshfunc
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

  encoded = np.array(map( lambda x: mywavelet.dwt(x,tensor=mytensor), data_float ))
  interdims = encoded[0].shape
  print "interdims:", interdims

  compression = find_cutoff_nd( encoded, mycompress )

  dicks = map( lambda x: mat_3d_to_dict( x, compression, mythreshfunc ), encoded )
  print map( lambda x: compress( x[0], x[1] ), zip( dicks, encoded ) )

  lists = map( lambda x: dict_to_mat_3d( x, interdims[0], interdims[1], interdims[2]), dicks )
  lists = map( lambda x: np.array(x), lists )

  decoded = map( lambda x: mywavelet.idwt(x,tensor=mytensor), lists )
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

  if myoutfile == None:
    filename = plaat.replace('.','_new.')
  else:
    filename = myoutfile
  print "Saving gif to",filename
  os.system(''.join(
    ["gifsicle -d ",
     str(mydelay),
     " --loopcount=forever -m ",
     "gif/temp.*.gif"
     ," > ",filename]))

  print "removing temp files"
  call(["rm"]+list(glob('gif/temp.*.gif')))
  call(["rm"]+list(glob('gif/temp.*.png')))

if __name__ == "__main__":
  # Dit stuk regelt de CLI options
  from sys import stderr
  import CLI,sys
  my_opts = [
    # short, long, args, description
    ('t','tensor',0,"zet tensor aan"),
    ('w','wavelet',1,"select wavelet <arg>"),
    ('s','smooth',0,"select quadratic thresholding"),
    ('c','compress',1,"set compression to <arg>"),
    ('o','output',1,"set destination to <arg>"),
    ('d','delay',1,"set frame-delay to <arg>"),
    ('h','help',0,'print this message')
  ]
  my_usage = CLI.usage("python animated_gif.py [gif] [options]",
                      "Uses various wavelets to compress and then decompress an animated gif",
                       my_opts)
  try:
    args, opts = CLI.parse_args(sys.argv,my_opts) #throws IOError on error
  except IOError:
    print my_usage.short()
    exit(1)

  #set defaults for various options
  from Wavelet_Defs import wavelet_dict
  mywavelet = wavelet_dict['haar']
  mycompress = 1.0
  myoutfile = None
  mytensor = False
  mydelay = 10
  mythreshfunc = threshold_hard

  for o in opts:
    if o[0] == 'wavelet':
      try:
        mywavelet = wavelet_dict[o[1]]
      except:
        print >>stderr,o[1],'is not a valid wavelet'
        exit(1)
    elif o[0] == 'compress':
      try:
        mycompress = float(o[1]) 
      except TypeError:
        exit(1)
    elif o[0] == 'output':
      myoutfile = o[1]
        
    elif o[0] == 'tensor':
      mytensor = True

    elif o[0] == 'help':
      print my_usage
      exit(1)
    elif o[0] == 'smooth':
      mythreshfunc = threshold_quad

    elif o[0] == 'delay':
      try:
        mydelay = int(o[1])
      except TypeError:
        exit(1)

  if len(args) == 1: # additional IOError
    print my_usage.short()
    exit(1)
  
  map(plaatje,args[1:])

