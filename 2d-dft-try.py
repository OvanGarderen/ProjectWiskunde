import cmath

def dft2dF( mat, M, N ):
    ret = [[ 0 for j in range(0,N)] for i in range(0,M)]

    coeff = 1.0/(M*N)

    for u in range(0,M):
        for v in range(0,N):
            ret[u][v] = sum(map(sum,
                                [[coeff * mat[x][y] * 
                                  cmath.exp(-2j * cmath.pi * ( (u*x)/(1.0*M) + (v*y)/(1.0*N) )) 
                                  for y in range(0,N) ] 
                                 for x in range(0,M) ]))
    return ret

def dft2df( mat, M, N ):
    mats = [[ mat[i][j] for j in range(0,len(mat[i])) ] 
            + [ 0 for j in range(len(mat[i]),N)] 
            for i in range(0,M) ]

    ret = [[ 0 for j in range(0,N)] for i in range(0,M)]

    for x in range(0,M):
        for y in range(0,N):
            ret[x][y] = sum(map(sum,
                                [[ mat[u][v] * 
                                  cmath.exp(2j * cmath.pi * ( (u*x)/(1.0*M) + (v*y)/(1.0*N) )) 
                                  for v in range(0,N) ] 
                                 for u in range(0,M) ]))

    return ret


if __name__ == "__main__":
    img = [ [0 + 2j,1+1j,2+0j], [2+0j,1+1j,0+2j], [1+1j,2+0j,0+2j] ]
    print img
    print
    coded = dft2dF( img, 3, 3 )
    uncoded = dft2df( coded, 3, 3 )
    print uncoded
    print
