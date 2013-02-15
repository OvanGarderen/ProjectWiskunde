import numpy as np
import math

class NotImplemented (Exception):
    pass

class Filter3D:
    encode_mat = [[[0,0],[0,0]],[[0,0],[0,0]]]
    decode_mat = [[[0,0],[0,0]],[[0,0],[0,0]]]
    typ = 'abstract 3D filter object'
    def __str__(self):
        return self.typ

    def apply(self,matrix):
        raise NotImplemented

class FilterSet3D:
    name = ''
    filt_low = None
    filt_high_list = [None,None,None,None]
    def filters(self):
        return [self.filt_low]+self.filt_high_list
    def __str__(self):
        return self.name

class Wav3D:
    name = ''
    filterset = None
    def __init__(self,name,filterset = None):
        self.name = name
        if filterset == None:
            try:
                self.filterset = filterdict[name]
            except:
                raise ValueError
        else:
            self.filterset = filterset

class HaarL3D (Filter3D):
    def __init__(self):
        c = math.sqrt(8)/8
        self.encode_mat = [[[c,c],[c,c]],[[c,c],[c,c]]]
        self.decode_mat = self.encode_mat
        self.typ = 'Haar 3D low pass filter'

class HaarH13D (Filter3D):
    def __init__(self):
        c = math.sqrt(8)/8
        self.coeff_mat = [[[c,0],[0,0]],[[0,0],[0,-c]]]
        self.decode_mat = map(lambda x: map(lambda y: map(lambda z: -z,y),x),[[[c,c],[c,c]],[[c,c],[c,c]]])
        self.typ = 'Haar 3D 1st high pass filter'

class HaarH23D (Filter3D):
    def __init__(self):
        c = math.sqrt(8)/8
        self.coeff_mat = [[[0,0],[c,0]],[[0,-c],[0,0]]]
        self.decode_mat = map(lambda x: map(lambda y: map(lambda z: -z,y),x),[[[c,c],[c,c]],[[c,c],[c,c]]])
        self.typ = 'Haar 3D 2nd high pass filter'

class HaarH33D (Filter3D):
    def __init__(self):
        c = math.sqrt(8)/8
        self.coeff_mat = [[[0,0],[0,c]],[[-c,0],[0,0]]]
        self.decode_mat = map(lambda x: map(lambda y: map(lambda z: -z,y),x),[[[c,c],[c,c]],[[c,c],[c,c]]])
        self.typ = 'Haar 3D 3rd high pass filter'

class HaarH43D (Filter3D):
    def __init__(self):
        c = math.sqrt(8)/8
        self.coeff_mat = [[[0,c],[0,0]],[[0,0],[-c,0]]]
        self.decode_mat = map(lambda x: map(lambda y: map(lambda z: -z,y),x),[[[c,c],[c,c]],[[c,c],[c,c]]])
        self.typ = 'Haar 3D 4th high pass filter'

class HaarSet3D (FilterSet3D):
    def __init__(self):
        self.name = "Haarset3D"
        self.filt_low = HaarL3D()
        self.filt_high_list = [HaarH13D(),HaarH23D(),HaarH33D(),HaarH43D()]

def split_seq(seq,n):
    return [seq[i:i+n] for i in range(0,len(seq),n)]

class Chunk3D:
    sizelog = 1
    mat = [[[]]]
    def __init__(self,data,breaksize=-1):
#if breaksize is not given, treat data as 3D matrix, else make data into matrix
        if breaksize <0:
            self.mat = data
            try:
                if len(data) == len(data[0]) and len(data[0]) == len(data[0][0]):
                    self.sizelog = len(data)
                else:
                    raise TypeError
            except:
                raise TypeError
        else:
            if len(data) != 2**(3*breaksize-3):
                print len(data)
                print 2**(3*breaksize-3)
                raise TypeError
            self.mat = split_seq(split_seq(data,2**(breaksize-1)),2**(breaksize-1))

    def split(self):
        chunks = []

        for x in self.mat:
            for y in x:
                chunks += y
        print chunks
        return chunks

    def __repr__(self):
        ret = ''
        ret+= '[\033[1;30mx)\033[0m '
        for i in self.mat:
            ret+= '\n[\033[1;32my)\033[0m\n '
            for j in i:
                ret+= '\t[\033[1;33mz)\033[0m '
                for k in j:
                    ret+= str(k)
                    ret+= ' '
                ret+= '] '
            ret+= '] '
        ret+= '] '
        return ret

filterdict = {'default' : HaarSet3D(), 'haar3d' : HaarSet3D()}

if __name__ == '__main__':
    wav = Wav3D('default')
    try:
        lel2 = Chunk3D([i for i in range(2**(3*2))],3)
        print lel2
        lulz = lel2.split()
        lulz1 = lulz[0]
        lulz2 = lulz[1]
        print lulz1
        print lulz2

    except NotImplemented:
        print '\'tis nog nie klaar lelleke'
