HEADER = "[Westerdiep/vanGarderen | V"
soFLOAT= 4
soINT = 4
PACKSTR= ">%dsi%dsici2sicx" % (len(HEADER),2)
PACKLEN= len(HEADER) + 4*soINT + 7

def wvg_save_v2( dict, dim, filename ):
    VERSION= 2
    import struct,sys,pickle
    M,N = dim

    size = 0
    head = struct.pack( PACKSTR ,HEADER,VERSION,"](",M,',',N,')[',size,']' )

    if filename == "stdout":
        f = sys.stdout
    else:
        f = open( filename, "w" ) 

    f.write(head)
    f.write( pickle.dumps(dict,pickle.HIGHEST_PROTOCOL) )
    f.write(";")
    
    if filename != "stdout":
        f.close()

def wvg_open_v2( filename ):
    VERSION = 2
    import struct,sys,pickle

    if filename == "stdin":
        f = sys.stdin
    else:
        f = open( filename, "r" ) 
    
    unp = f.read( PACKLEN )
    header = struct.unpack( PACKSTR , unp )
    
    if header[0] != HEADER :
        print >>sys.stderr,header[0],"is not a valid Westerdiep/vanGarderen imagefile"
        raise IOError
    if header[1] != VERSION :
        print >>sys.stderr,header[1],"is an incorrect version number"
    
    dim = (header[3],header[5])

    dict = pickle.loads( f.read() )
        
    if filename != "stdin":
        f.close()

    return dict,dim
