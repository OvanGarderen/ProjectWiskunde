from Wavelets import HaarWavelet as haar
from Wavelets import Daubechies2Wavelet as db2
from Wavelets import BiOrtho97Wavelet as bo97
from Wavelets import BiOrtho97Wavelet as bo53
from db40 import Daubechies40Wavelet as db40

wavelet_dict = {
    'db2' : db2,
    'haar' : haar,
    'bo97' : bo97,
    'bo53' : bo53,
    'db40' : db40
}
