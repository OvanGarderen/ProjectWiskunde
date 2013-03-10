import cmath

def dft(x):
  N = len(x)
  X = []
  for k in range(N):
    X_k = 0
    for n in range(N):
      X_k += x[n] * cmath.exp(-1j * 2 * cmath.pi * k * n / N )
    X.insert(k, X_k)
  return X

def idft(X):
  N = len(X)
  x = []
  for n in range(N):
    x_n = 0
    for k in range(N):
      x_n += X[k] * cmath.exp(1j * 2 * cmath.pi * k * n / N )
    x.insert(n, x_n/N)
  return x

def twoddft(x):
  N = len(x)
  X = []
  for n in range(N):
    X.insert(n, dft(x[n]))
  return X

def twodidft(x):
  N = len(x)
  X = []
  for n in range(N):
    X.insert(n, idft(x[n]))
  return X

def img2mat(name):
  raw = Image.open(name)
  img = list(raw.convert('1').getdata())

  img_mat = []
  for i in range(raw.size[1]):
    c = img[:raw.size[0]]
    img = img[raw.size[0]:]
    img_mat.append( c )

  return img_mat

def mat2img(data,size):
  from PIL import Image
  imgl = []
  for x in data:
    imgl +=x
  i = Image.new('1',size)
  i.putdata(imgl)
  return i

if __name__ == "__main__":
  from PIL import Image
  img = img2mat("rubiks.jpg") 

  x = [[0.0, 0.5], 
       [0.2, 0.8]]
  X = twoddft(img)
  x_ = map(lambda x: map(lambda y: y.real,x),twodidft(X))

  mat2img(x_,(60,60)).save("cubecompressed.png")

