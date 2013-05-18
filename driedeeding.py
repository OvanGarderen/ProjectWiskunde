from PIL import Image
from channels import listtomat
from Wavelets import HaarWavelet as haar
import images2gif as gifs

import sys

def processImage(infile):
    im = Image.open(infile)
    mypalette = im.getpalette()
    driedlist = [[],[],[],[]]

    frames = gifs.readGif(infile,True)
    for frame in frames:
        print frame.shape

#    print "chan, frames, height, width:\n",len(driedlist),len(driedlist[0]),len(driedlist[0][0]),len(driedlist[0][0][0])
    return (driedlist, (len(driedlist[0][0]), len(driedlist[0][0][0])))

if __name__ == "__main__":
    name = sys.argv[1]
    data, dim = processImage(name)
"""
    mywavelet = haar
  
    data = map(lambda x: np.array(x), data)
    data_float = map(lambda x: x.astype('float'),data)

    print "Starting encoding of image %s" % (argv[1])
    print "Image has dimensions : %i,%i" % dim
    print

    encoded = map(mywavelet.dwt,data_float)
    interdims = (len(encoded[0]),len(encoded[0][0]))

    print "Encoding done"
    #  print_dimensions_matlist("Encoded dims:",encoded)
    print "Using dimensions:",interdims
    print

    "" Temporary bypass to check for problems in main algorithm -- Confirmed 
    compression = 0.0

    print "Converted to dictionaries:"
    print "Compression cutoff is %f" % compression

    dicks = map(lambda x: mat5dict(x,compression),encoded)

    print "Dictionary lengths:"
    for x in dicks: 
      print len(x)

    print "Compression factor per channel:"
    print map(lambda x: compress(x[0],x[1]), zip(dicks,encoded))
    print

    print "Converting dictionaries to matrices"
    print "Dimensions are %i,%i" % interdims

    lists = map(lambda x: dict5mat(x,interdims[0],interdims[1]),dicks)  
    lists = map(lambda x: np.array(x), lists)
    ""
    print "Starting decoding"

    decoded = map(mywavelet.idwt,encoded)

    print "Decoding done"  
    #  print_dimensions_matlist("Decoded dimensions are:",decoded)
    #  print

    sliced = map(lambda x: np.rint(x).astype(data[0].dtype),decoded)

    #  print_dimensions_matlist("Sliced dimensions are:",sliced)

    filename = argv[1].replace('.','_new.')
    print "Saving to",filename
    mat5img(sliced,dim).save(filename)
"""
