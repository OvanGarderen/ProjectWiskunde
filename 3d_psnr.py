from subprocess import call
import sys
from glob import glob
from channels import *
import numpy as np
from PSNR import PSNR
import matplotlib.pyplot as plt

def zure_routine(lijst):
  for i in lijst:
    if i == "1":
      return 0.1
    if i == "2":
      return 0.2
    if i == "02":
      return 0.02
ref = sys.argv[1]
names = sys.argv[2:]
data_list = []

if len( glob("tmp/"+ref+".*")) == 0:
  call(["gifsicle", "--unoptimize", "-e", ref, "-o", "tmp/"+ref])
gifs = sorted(glob("tmp/"+ref+".*"))
lijst = [[],[],[],[]]

for f in gifs:
  data, dim = img3mat( f)
  for i in range( len( data )):
    lijst[i].append(data[i])

data = np.array(map( lambda x: np.array(x), lijst ))

for name in names:
  if len( glob("tmp/"+name+".*")) == 0:
    call(["gifsicle", "--unoptimize", "-e", name, "-o", "tmp/"+name ])
  gifs2 = sorted(glob("tmp/"+name+".*"))
  lijst2 = [[],[],[],[]]

  for f in gifs2:
    data2, dim = img3mat( f)
    for i in range( len(data)):
      lijst2[i].append(data2[i])
  data2 = np.array( map( lambda x: np.array(x), lijst2 ) )

  print data.shape, data2.shape
  data_list.append( (PSNR(data, data2), name))

plot_haar = [[],[]]
plot_haar_t = [[],[]]
plot_db2 = [[],[]]
plot_db2_t = [[],[]]
for i in range( len( data_list ) ):
  psnr, name = data_list[i]
  lijst = None
  value = 0.0
  if "haar" in name:
    if "tensor" in name:
      lijst = plot_haar_t
    else:
      lijst = plot_haar
  else:
    if "tensor" in name:
      lijst = plot_db2_t
    else:
      lijst = plot_db2

  value = zure_routine(name.split("_"))
  print name, value, psnr
  lijst[0].append(value)
  lijst[1].append(psnr)

plt.plot(plot_haar[0], plot_haar[1], label="Haar")
plt.plot(plot_haar_t[0], plot_haar_t[1], label="Haar Tensor")
plt.plot(plot_db2[0], plot_db2[1], label="Daubechies 2")
plt.plot(plot_db2_t[0], plot_db2_t[1], label="Daubechies 2 Tensor")
plt.title(ref)
plt.legend(loc=2)
plt.show()
