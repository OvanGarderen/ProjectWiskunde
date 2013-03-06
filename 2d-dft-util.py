import cmath
import numpy as np

VERSION = 1

def dft2dF( mat, dim ):
    M, N = dim
    cuttof = 10
    ret = [[] for i in range(0,M)]

    coeff = 1.0/(M*N)

    for u in range(0,M):
        for v in range(0,N):
            a = sum(map(sum,
                        [[coeff * mat[x][y] * 
                          cmath.exp(-2j * cmath.pi * ( (u*x)/(1.0*M) + (v*y)/(1.0*N) )) 
                          for y in range(0,N) ] 
                         for x in range(0,M) ]))
            if abs(a) > cuttof:
                ret[u].append(a)
            else:
                break
    return ret

def dft2df( mat, dim ):
    M, N = dim
    mats = [[ mat[i][j] for j in range(0,len(mat[i])) ] 
            + [ 0 for j in range(len(mat[i]),N)] 
            for i in range(0,M) ]

    ret = [[ 0 for j in range(0,N)] for i in range(0,M)]

    for x in range(0,M):
        print x
        for y in range(0,N):
            ret[x][y] = sum(map(sum,
                                [[ mats[u][v] * 
                                  cmath.exp(2j * cmath.pi * ( (u*x)/(1.0*M) + (v*y)/(1.0*N) )) 
                                  for v in range(0,N) ] 
                                 for u in range(0,M) ])).real

    return ret

def pr_mat( mat, col ):
    for i in mat:
        print '\t\033[%dm' % (col),i
    print '\033[0m'

def img2mat(name):
    from PIL import Image
    raw = Image.open(name)
    img = list(raw.convert('L').getdata())

    print img[0]
    
    img_mat = []
    for i in range(raw.size[1]):
        c = img[:raw.size[0]]
        img = img[raw.size[0]:]
        img_mat.append( c )
        
    return (img_mat,raw.size)

def mat2img(data,size):
    from PIL import Image
    imgl = []
    for x in data:
        imgl +=x
    i = Image.new('L',size)
    i.putdata(imgl)
    return i

HEADER = "[Westerdiep/vanGarderen | V"
soFLOAT= 4
soINT = 4
PACKSTR= ">%dsi%dsici2sicx" % (len(HEADER),2)
PACKLEN= len(HEADER) + 4*soINT + 7

def savencoded( data, dim, filename ):
    import struct
    M,N = dim

    size = sum(map(sum,[[ 1 for j in i] for i in data ])) + len(data)
    head = struct.pack( PACKSTR ,HEADER,VERSION,"](",M,',',N,')[',size,']' )

    with open( filename, "w" ) as f:
        f.write(head)
        for row in data:
            f.write( struct.pack('i', 2*len(row) ) )
            for entry in row:
                f.write( struct.pack("ff",entry.real,entry.imag) )
        f.write(";")

def openencoded( filename ):
    import struct

    with open( filename, "r" ) as f:
        unp = f.read( PACKLEN )
        header = struct.unpack( PACKSTR , unp )

        if header[0] != HEADER :
            print header[0],"is not a valid Westerdiep/vanGarderen imagefile"
            raise IOError
        if header[1] != VERSION :
            print header[1],"is an incorrect version number"
        
        dim = (header[3],header[5])
        readsize = header[7]*soFLOAT + 1
        imgdata = f.read()

        print dim
        
        img = []
        for i in range(dim[0]):
            size = struct.unpack('i', imgdata[:soINT] )[0]
            line = imgdata[soINT:soINT + soFLOAT*size]
            imgdata = imgdata[soINT + soFLOAT*size:]
            ls = []
            for j in range(size/2):
                a = struct.unpack("2f", line[:2*soFLOAT] )
                line = line[2*soFLOAT:]
                ls.append(a[0] + a[1]*1j)
            img.append(ls)
            
    return img,dim

def raw_save( data, dim, filename ):
    with open(filename + ".rel","w") as f:
        f.write( str(dim) + '\n')
        for row in data:
            for entry in row:
                f.write( str(entry) )
                f.write("|")
            f.write("\n")
    print "saved file",filename,".rel"

def raw_load( filename ):
    import struct
    with open(filename + ".rel","r") as f:
        dim = map(int,f.readline().replace('(','').replace(')','').split(','))
        a = f.readlines()
        c = map(lambda x: map(complex,x.split('|')[:-1]),a)
    return c,dim

if __name__ == "__main__":
    import sys
    if(len(sys.argv) < 2):
        openencoded( "encoded.wvg" )
        exit(1)

    if sys.argv[1] == "decode" :
        data,dim = openencoded( sys.argv[2] )
        im = mat2img( dft2df( data, dim ), dim )
        im.save( sys.argv[3] )
        exit(1)

    if sys.argv[1] == "rawenc" :
        data,dim = raw_load( sys.argv[2] )
        savencoded( data, dim, sys.argv[3] )
        exit(1)
            
    img,dim = img2mat(sys.argv[1])
    coded = dft2dF( img, dim )
    
    raw_save(coded, dim, "enc")

    savencoded(coded,dim,"encoded.wvg")

    uncoded = dft2df( coded, dim )

    im = mat2img( uncoded, dim )
    im.save("wefuckenallesop*yay*.jpg")
