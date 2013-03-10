import cmath

def dft2dF( mat, M, N ):
    cuttof = 0
    ret = [[] for i in range(0,M)]

    coeff = 1.0/(M*N)

    for u in range(0,M):
        for v in range(0,N):
            a = sum(map(sum,
                        [[coeff * mat[x][y] * 
                          cmath.exp(-2j * cmath.pi * ( (u*x)/(1.0*M) + (v*y)/(1.0*N) )) 
                          for y in range(0,N) ] 
                         for x in range(0,M) ]))
            if abs(a) > cuttof:
                ret[u].append(a)
            else:
                break
    return ret

def dft2df( mat, M, N ):
    mats = [[ mat[i][j] for j in range(0,len(mat[i])) ] 
            + [ 0 for j in range(len(mat[i]),N)] 
            for i in range(0,M) ]

    pr_mat( mats, 31)

    ret = [[ 0 for j in range(0,N)] for i in range(0,M)]

    for x in range(0,M):
        for y in range(0,N):
            ret[x][y] = sum(map(sum,
                                [[ mats[u][v] * 
                                  cmath.exp(2j * cmath.pi * ( (u*x)/(1.0*M) + (v*y)/(1.0*N) )) 
                                  for v in range(0,N) ] 
                                 for u in range(0,M) ])).real

    return ret

def pr_mat( mat, col ):
    for i in mat:
        print '\t\033[%dm' % (col),i
    print '\033[0m'

def img2mat(name):
    from PIL import Image
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
    import sys
    if(len(sys.argv) < 2):
        exit(1)

    img = img2mat(sys.argv[1])
    pr_mat(img,32)

    coded = dft2dF( img, 60, 60 )
    pr_mat(coded,31)

    uncoded = dft2df( coded, 60, 60 )
    pr_mat(uncoded,32)

    im = mat2img( uncoded, (60,60) )
    im.save("wefuckenallesop*yay*.jpg")
