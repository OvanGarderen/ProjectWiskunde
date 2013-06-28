import numpy as np
import matplotlib.pyplot as plt

fake_list = [
{
  'label': "hoi1",
  'psnr': [-33,-32,-31],
  'ratios': [0.1, 0.2, 0.5]
},
{
  'label': "hoi2",
  'psnr': [2,5,6],
  'ratios': [0.1, 0.2, 0.5]
},
{
  'label': "hoi3",
  'psnr': [1,2,3],
  'ratios': [0.1, 0.2, 0.5]
},

]

for i in range( len( fake_list ) ):
  lst = fake_list[i]
  print lst
  plt.plot(lst['ratios'], lst['psnr'], label=lst['label'] )
plt.legend()
plt.show()
