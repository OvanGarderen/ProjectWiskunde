#!/usr/bin/python

import numpy as np
from ImageUtils import plaatje
from Wavelets import HaarWavelet
from sys import argv

def main():
  if len(argv) < 2:
    print "Usage: waveworker.py filename [compression]"
    return None

  #process imput arguments
  filename = argv[1]
  newfilename = filename.replace('.','_new.')

  if len(argv) > 2:
    compression = float(argv[2])
  else:
    compression = 0.0

  #main process
  print "Loading Image"
  
  img = plaatje(filename = filename)
  img.type_convert('float')
  print img.data
  print img.filename
  print img.dim
  print img.kanalen

  print "Started encoding"

  enc_img = img.mapto_channels(HaarWavelet.dwt)

  print "Encoding done"
  print "Started decoding"

  dec_img = enc_img.mapto_channels(HaarWavelet.idwt)

  print "Decoding done"  

  dec_img.type_convert('int')
  dec_img.saveas(filename,newfilename)
  
if __name__ == "__main__":
  main()
