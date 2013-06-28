def run_and_print(comm):
    from subprocess import Popen,check_call,check_output
    print 'running',' '.join(comm)
    child = Popen(comm)
    return child

def do_graphics(compressions):
    global myinfile,myskip,mytensor
    print "doing compression with ratios",compressions
    
    map(float,compressions) # catches errors

    names_fourier = map(lambda x: myinfile[:-4] + '_' + 'fourier' 
                        + '_' + str(x).replace('.','_') + myinfile[-4:],
                        compressions)
    names_haar = map(lambda x: myinfile[:-4] + '_' + 'haar' 
                        + '_' + str(x).replace('.','_') + myinfile[-4:],
                        compressions)
    names_db2 = map(lambda x: myinfile[:-4] + '_' + 'db2' 
                        + '_' + str(x).replace('.','_') + myinfile[-4:],
                        compressions)
    names_haar_t = map(lambda x: myinfile[:-4] + '_' + 'haar_t' 
                        + '_' + str(x).replace('.','_') + myinfile[-4:],
                        compressions)
    names_db2_t = map(lambda x: myinfile[:-4] + '_' + 'db2_t' 
                        + '_' + str(x).replace('.','_') + myinfile[-4:],
                        compressions)

    from os.path import isfile
    bullshit = ['echo','check em']

    commlist_fourier = map(lambda x: ['python2','3chan.py','-c',x[0],'-o',x[1],myinfile] 
                           if not isfile(x[1]) else bullshit,
                           zip(compressions,names_fourier))
    commlist_haar = map(lambda x: ['python2','wave_img.py','-w','haar','--smooth',
                                  '-c',x[0],'-o',x[1],myinfile]
                        if not isfile(x[1]) else bullshit,
                        zip(compressions,names_haar))
    commlist_db2 = map(lambda x: ['python2','wave_img.py','-w','db2','--smooth',
                                  '-c',x[0],'-o',x[1],myinfile]
                       if not isfile(x[1]) else bullshit,
                       zip(compressions,names_db2))
    commlist_haar_t = map(lambda x: ['python2','wave_img.py','--tensor','-w','haar',
                                     '--smooth','-c',x[0],'-o',x[1],myinfile]
                        if not isfile(x[1]) else bullshit,
                          zip(compressions,names_haar_t))
    commlist_db2_t = map(lambda x: ['python2','wave_img.py','--tensor','-w','db2','--smooth',
                                  '-c',x[0],'-o',x[1],myinfile]
                       if not isfile(x[1]) else bullshit,
                         zip(compressions,names_db2_t))
 
    if not myskip:
        ch_1 = map(run_and_print,commlist_fourier)
        map(lambda x: x.wait(),ch_1)
        ch_2 = map(run_and_print,commlist_haar)
        map(lambda x: x.wait(),ch_2)
        ch_3 = map(run_and_print,commlist_db2)
        map(lambda x: x.wait(),ch_3)
        ch_4 = map(run_and_print,commlist_haar_t)
        map(lambda x: x.wait(),ch_4)
        ch_5 = map(run_and_print,commlist_db2_t)
        map(lambda x: x.wait(),ch_5)

    from PSNR import do_PSNR
    imges_fourier = do_PSNR(['',myinfile]+names_fourier)
    imges_db2 = do_PSNR(['',myinfile]+names_db2)
    imges_haar = do_PSNR(['',myinfile]+names_haar)
    imges_db2_t = do_PSNR(['',myinfile]+names_db2_t)
    imges_haar_t = do_PSNR(['',myinfile]+names_haar_t)

    print imges_fourier
    print imges_haar
    print imges_db2
    print imges_haar_t
    print imges_db2_t

    psnr_fourier = map(lambda x: x[0], imges_fourier)
    psnr_haar = map(lambda x: x[0], imges_haar)
    psnr_db2 = map(lambda x: x[0], imges_db2)
    psnr_haar_t = map(lambda x: x[0], imges_haar_t)
    psnr_db2_t = map(lambda x: x[0], imges_db2_t)

    ratios = map(lambda x: x, compressions)

    real_list = [
        {
            'label':'Fourier',
            'psnr':psnr_fourier,
            'ratios':ratios
        },
        {
            'label':'Haar',
            'psnr':psnr_haar,
            'ratios':ratios
        },
        {
            'label':'Daubechies 2',
            'psnr':psnr_db2,
            'ratios':ratios
        }
    ]
    if mytensor:
        real_list += [
        {
            'label':'Haar (Tensor)',
            'psnr':psnr_haar_t,
            'ratios':ratios
        },
        {
            'label':'Daubechies 2 (Tensor)',
            'psnr':psnr_db2_t,
            'ratios':ratios
        }]
    import matplotlib.pyplot as plt
    for i in range( len( real_list )):
        lst = real_list[i]
        plt.plot(lst['ratios'],lst['psnr'],label=lst['label'])
    plt.title(myinfile)
    plt.legend(loc=2)
    plt.show()

if __name__=="__main__":
    from sys import stderr
    import CLI,sys
    my_opts = [
        # short, long, args, description
        ('p','psnr',0,'skips to PSNR calc'),
        ('t','tensor',1,'tensor ja/nee ja!'),
        ('i','infile',1,"set infile to <arg>"),
        ('h','help',0,'print this message')
    ]
    my_usage = CLI.usage("maek_graphics.py [-i picture] <compressions>",
                         "Makes fancy gaphics",
                         my_opts)
    try:
        args, opts = CLI.parse_args(sys.argv,my_opts) #throws IOError on error
    except IOError:
        print my_usage.short()
        exit(1)

    from Wavelet_Defs import wavelet_dict
    mytensor = False
    myinfile = None
    myskip = False

    for o in opts:
        if o[0] == 'tensor':
            mytensor = True
        elif o[0] == 'psnr':
            myskip = True
        elif o[0] == 'infile':
            myinfile = o[1]
        elif o[0] == 'help':
            print my_usage
            exit(1)

    if len(args) == 1: # additional IOError
        print my_usage.short()
        exit(1)
  
    do_graphics(args[1:])

