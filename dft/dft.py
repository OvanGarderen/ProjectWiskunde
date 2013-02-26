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

if __name__ == "__main__":
  from PIL import Image
  img = Image.open("rubiks.jpg")
  print img
  x = [[0.0, 0.5], 
       [0.2, 0.8]]
  X = twoddft(x)
  x_ = twodidft(X)
  print x, X, x_
