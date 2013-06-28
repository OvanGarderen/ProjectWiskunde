from PIL import Image

def listtomat( ls, scl ):
    return [ ls[i*scl : (i+1) * scl] for i in xrange(len(ls)/scl)]

def img3mat( filename ):
    img = Image.open(filename).convert('RGBA')
    img.load()
    rgbtuple = map(lambda x: x.getdata(), img.split())

    rgb = map(list,rgbtuple)
    rgbmat = map(lambda x: listtomat(x,img.size[1]),rgb)

    return (rgbmat,(img.size[1],img.size[0]))

def mat3img( data, size ):
    rgb = map(lambda z: reduce(lambda x,y: x+y,z), data)

    tuplist = []
    for i in xrange(len(rgb[0])):
        tuplist.append( tuple([ls[i] for ls in rgb]) )

    #print len(tuplist),len(tuplist[0])

    img = Image.new('RGBA'[:len(tuplist)],(size[1],size[0]))
    img.putdata(tuplist)
    return img

def compress( dicks, mats):
    import numpy as np
    mats = np.array(mats)
    return float(len(dicks))/reduce(lambda x, y: x * y, mats.shape)


def main(imgname):
    global mycompress,myoutfile

    from FFT2util import FFT2D,iFFT2D,matslice,realintmat
    from FFTjan import mat2dict,dict2mat
    from Tools import find_cutoff_nd

    data, dim = img3mat(imgname)

    print "starting encoding of image %s" % (imgname)
    encoded = map(FFT2D,data)
    print "encoding succesfull"

    dim2 = (len(encoded[0][0]),len(encoded[0]))
    print dim2

    import numpy as np
    cutoff = find_cutoff_nd( np.array(encoded), mycompress )

    print "making dicks"
    dicks = map(lambda x: mat2dict(x,cutoff),encoded)
    
    print len(dicks[0])
    
    print map(lambda x: compress(x[0],x[1]), zip(dicks,encoded))

    print "listing dicks"
    lists = map(lambda x: dict2mat(x,dim2[0],dim2[1]),dicks)
    
    print "starting decoding"
    decoded = map(iFFT2D,lists)
    
    print "decoding succesfull"
    sliced = map(lambda x: matslice(realintmat(x),dim),decoded)

    if myoutfile != None:
        filename = myoutfile
    else:
        filename = imgname.replace('.','_new.')
    print "saving to",filename
    mat3img(sliced,dim).save(filename)

if __name__=="__main__":
  # Dit stuk regelt de CLI options
  from sys import stderr
  import CLI,sys
  my_opts = [
    # short, long, args, description
    ('s','smooth',0,"activate quadratic threshold"),
    ('c','compress',1,"set compression to <arg>"),
    ('o','output',1,"set destination to <arg>"),
    ('h','help',0,'print this message')
  ]
  my_usage = CLI.usage("3chan.py [picture] [options]",
                       "Uses various wavelets to compress and then decompress a picture",
                       my_opts)
  try:
    args, opts = CLI.parse_args(sys.argv,my_opts) #throws IOError on error
  except IOError:
    print my_usage.short()
    exit(1)

  #set defaults for various options
  from Wavelet_Defs import wavelet_dict
  mycompress = 1.0
  myoutfile = None

  for o in opts:
    if o[0] == 'compress':
      try:
        mycompress = float(o[1]) 
      except TypeError:
        exit(1)
    elif o[0] == 'output':
      myoutfile = o[1]
    elif o[0] == 'help':
      print my_usage
      exit(1)

  if len(args) == 1: # additional IOError
    print my_usage.short()
    exit(1)
  
  map(main,args[1:])

