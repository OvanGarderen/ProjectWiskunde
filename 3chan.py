from PIL import Image

def listtomat( ls, scl ):
    return [ ls[i*scl : (i+1) * scl] for i in xrange(len(ls)/scl)]

def img3mat( filename ):
    img = Image.open(filename)
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

    print len(tuplist),len(tuplist[0])

    img = Image.new('RGBA'[:len(tuplist)],(size[1],size[0]))
    img.putdata(tuplist)
    return img

def compress( dicks, mats):
    return float(len(dicks))/reduce(lambda x, y: x * y, mats.shape)


if __name__=="__main__":
    from sys import argv
    from FFT2util import FFT2D,iFFT2D,matslice,realintmat
    from FFTjan import mat2dict,dict2mat

    data, dim = img3mat(argv[1])

    print "starting encoding of image %s" % (argv[1])
    encoded = map(FFT2D,data)
    print "encoding succesfull"

    dim2 = (len(encoded[0][0]),len(encoded[0]))
    print dim2

    print "making dicks"
    dicks = map(lambda x: mat2dict(x,0.15),encoded)
    
    print len(dicks[0])
    
    print map(lambda x: compress(x[0],x[1]), zip(dicks,encoded))

    print "listing dicks"
    lists = map(lambda x: dict2mat(x,dim2[0],dim2[1]),dicks)
    
    print "starting decoding"
    decoded = map(iFFT2D,lists)
    
    print "decoding succesfull"
    sliced = map(lambda x: matslice(realintmat(x),dim),decoded)
    
    mat3img(sliced,dim).save(argv[1].replace('.','_new.'))
