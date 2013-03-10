import cmath,math,copy
import numpy as np
from DFTutil import *

from cmath import pi

VERSION = 1

def _FFT( ls ):
    N = len(ls)
    ls += [0 for i in range( minimaxpow2(N) - N)]
    return FFT(ls)

def FFT( ls ):
    N = len(ls)
    if N <= 1: 
        return ls
    else:
        even = FFT(ls[0::2])
        odd  = FFT(ls[1::2])
        return [( even[k] + cmath.exp(-2j*pi*k/N)*odd[k] )*0.5 for k in xrange(N/2)] + \
            [( even[k] - cmath.exp(-2j*pi*k/N)*odd[k] )*0.5 for k in xrange(N/2)]

def iFFT( ls ):
    N = len(ls)
    if N <= 1: 
        return ls
    else:
        even = iFFT(ls[0::2])
        odd  = iFFT(ls[1::2])
        return [even[k] + cmath.exp(2j*pi*k/N)*odd[k] for k in xrange(N/2)] + \
            [even[k] - cmath.exp(2j*pi*k/N)*odd[k] for k in xrange(N/2)]

def _FFT2D( _mat ):
    mat = matpow2_zero(_mat)
    return FFT2D(mat)
    
def _iFFT2D( _mat ):
    mat = matpow2_zero(_mat)
    return iFFT2D(mat)

def FFT2D( _mat ):
    M = len(_mat)
    N = len(_mat[0])

    mat = copy.deepcopy(_mat)

    # FFT on rows
    mat = map( FFT, mat )

    # FFT on columns
    mat = transpose(mat)
    mat = map( FFT, mat )
    mat = transpose(mat)

    return mat

def iFFT2D( _mat ):
    M = len(_mat)
    N = len(_mat[0])

    mat = copy.deepcopy(_mat)

    # inverse FFT on rows
    mat = map( FFT, mat )

    # inverse FFT on columns
    mat = transpose(mat)
    mat = map( iFFT, mat )
    mat = transpose(mat)

    return mat

def pr_matdims( mat ):
    import sys
    dim = (len(mat), min([len(mat[x]) for x in range(len(mat))]), max([len(mat[x]) for x in range(len(mat))]))
    print >>sys.stderr,"matrix is of size %d by %d to %d" % dim

def matpow2_repeat( _mat ):
    import math,copy
    mat = copy.deepcopy(_mat)
    N,M = (len(mat), max([len(mat[x]) for x in xrange(len(mat))]))
    mat += [ mat[i] for i in xrange( minimaxpow2( N ) - N)]
    mat = map(lambda x: x + [ x[i] for i in xrange( minimaxpow2(M) - len(x))], mat)
    return mat

def matpow2_zero( _mat ):
    import copy
    mat = copy.deepcopy(_mat)
    N,M = (len(mat), max([len(mat[x]) for x in xrange(len(mat))]))
    mat += [ [0 for j in xrange(M)] for i in xrange( minimaxpow2( N ) - N)]
    mat = map(lambda x: x + [ 0 for i in xrange( minimaxpow2(M) - len(x))], mat)
    return mat

def minimaxpow2( a ):
    import math
    return 2**int(math.ceil(math.log(a,2)))

def matslice( mat, dim, offset = (0,0), step=(1,1) ):
    return map(lambda x: x[offset[1]:dim[1]:step[1]], mat[offset[0]:dim[0]:step[0]])

def transpose( mat ):
    return [[ mat[x][y] for x in range(len(mat))] for y in range(len(mat[0]))] 

def realintmat( mat ):
    return map(lambda x: map(lambda y: int(round(y.real)),x),mat)

def rowcompress( mat, cutoff ):
    ret = []
    for row in mat:
        r = []
        i = 0
        while i<len(row) and abs(row[i]) > cutoff:
            r.append(row[i])
            i+=1
        ret.append(r)
    print len(ret),sum([len(ret[x]) for x in range(len(ret))])
    return ret

def cond_print( stri, cond ):
    import sys
    if cond:
        print >>sys.stderr,stri

if __name__ == "__main__":
    import math,sys

    mode = ''
    fi = 'stdin'
    fo = 'stdout'
    compr = 0.0001
    verbose = False

    if '-v' in sys.argv:
        verbose = True

    if '-d' in sys.argv:
        mode = 'decode'
        cond_print( "mode set to decoding", verbose ) 
    elif '-e' in sys.argv:
        mode = 'encode'
        cond_print( "mode set to encoding", verbose ) 
    else:
        print 'usage:',sys.argv[0],'-d/-e [-i infile] [-c compression] [-o outfile]'
        exit(1)

    if '-c' in sys.argv:
        ind = sys.argv.index('-c') + 1
        if ind > len(sys.argv):
            print 'option -c expects an argument'
        compr = float(sys.argv[ind])

    cond_print( "compression is %f " % (compr), verbose ) 
    
    if '-i' in sys.argv:
        ind = sys.argv.index('-i') + 1
        if ind > len(sys.argv):
            print 'option -i expects an argument'
        fi = sys.argv[ind]
        cond_print( "reading from file " + fi, verbose ) 
    if '-o' in sys.argv:
        ind = sys.argv.index('-o') + 1
        if ind > len(sys.argv):
            print 'option -o expects an argument'
        fo = sys.argv[ind]
        cond_print( "writing to file " + fo, verbose ) 

    if mode == 'decode':
        dat, dim = openencoded( fi )
        cond_print( "got file (%d,%d) " % dim, verbose ) 
        dec = matslice( realintmat( _iFFT2D( dat ) ), dim )
        if fo == 'stdout':
            cond_print( "printing to stdout", verbose ) 
            print dec
        else:
            cond_print( "saving to %s" % fo, verbose ) 
            mat2img(dec,dim).save( fo )
    elif mode == 'encode':
        if fi == 'stdin':
            print "reading from stdin not supported"
            exit(1)
        dat, dim = img2mat( fi )
        cond_print( "got file (%d,%d) " % dim, verbose ) 
        enc = rowcompress( _FFT2D( dat ), compr )
        cond_print( "saving to %s" % fo, verbose ) 
        savencoded( enc, dim, fo )

