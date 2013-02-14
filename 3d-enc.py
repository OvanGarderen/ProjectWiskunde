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
        
filterdict = {'default' : HaarSet3D(), 'haar3d' : HaarSet3D()}

if __name__ == '__main__':

    data = [[[1,1],[1,1]],[[1,1],[1,1]]]

    wav = Wav3D('default')
    print wav.filterset,'applied to',data,'gives'

    try:
        for filt in wav.filterset.filters():
            print filt.apply(data)

    except NotImplemented:
        print '\'tis nog nie klaar lelleke'
