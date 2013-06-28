#!/bin/bash

NAME=$1
FILE=$(ls -1 plaatjes | egrep "$NAME.jpg|$NAME.png" -m 1 )

echo $FILE

python2 FFT2util.py -v -e -i "plaatjes/$FILE" -o "plaatjes/$NAME.wvg" && python2 FFT2util.py -v -d -i "plaatjes/$NAME.wvg" -o "plaatjes/U$NAME.jpg"
