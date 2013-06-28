def run_and_print(comm):
    from subprocess import Popen,check_call,check_output
    print 'running',' '.join(comm)
    child = Popen(comm)
    return child

def do_graphics(compressions):
    global myinfile,myskip
    print "doing compression with ratios",compressions
    
    map(float,compressions) # catches errors

    names_fourier = map(lambda x: myinfile[:-4] + '_' + 'fourier' 
                        + '_' + str(x) + myinfile[-4:],
                        compressions)
    names_haar = map(lambda x: myinfile[:-4] + '_' + 'haar' 
                        + '_' + str(x) + myinfile[-4:],
                        compressions)
    names_db2 = map(lambda x: myinfile[:-4] + '_' + 'db2' 
                        + '_' + str(x) + myinfile[-4:],
                        compressions)

    from os.path import isfile

    commlist_fourier = map(lambda x: ['python2','3chan.py','-c',str(x[0]),'-o',x[1],myinfile] 
                           if not isfile(x[1]) else ['sleep','1'],
                           zip(compressions,names_fourier))
    commlist_haar = map(lambda x: ['python2','wave_img.py','-w','haar','--smooth',
                                  '-c',x[0],'-o',x[1],myinfile]
                        if not isfile(x[1]) else ['sleep','1'],
                        zip(compressions,names_haar))
    commlist_db2 = map(lambda x: ['python2','wave_img.py','-w','db2','--smooth',
                                  '-c',x[0],'-o',x[1],myinfile]
                       if not isfile(x[1]) else ['sleep','1'],
                       zip(compressions,names_db2))
 
    if not myskip:
        ch_1 = map(run_and_print,commlist_fourier)
        ch_2 = map(run_and_print,commlist_haar)
        ch_3 = map(run_and_print,commlist_db2)

        map(lambda x: x.wait(),ch_1+ch_2+ch_3)

    from PSNR import do_PSNR
    imges_fourier = do_PSNR(['',myinfile]+names_fourier)
    imges_db2 = do_PSNR(['',myinfile]+names_db2)
    imges_haar = do_PSNR(['',myinfile]+names_haar)

    print imges_fourier
    print imges_haar
    print imges_db2

    psnr_fourier = map(lambda x: x[0], imges_fourier)
    psnr_haar = map(lambda x: x[0], imges_haar)
    psnr_db2 = map(lambda x: x[0], imges_db2)

    real_list = [
        {
            'label':'Fourier',
            'psnr':psnr_fourier,
            'ratios':compressions
        },
        {
            'label':'Haar',
            'psnr':psnr_haar,
            'ratios':compressions
        },
        {
            'label':'Daubechies 2',
            'psnr':psnr_db2,
            'ratios':compressions
        },
    ]
    import matplotlib.pyplot as plt
    for i in range( len( real_list )):
        lst = real_list[i]
        plt.plot(lst['ratios'],lst['psnr'],label=lst['label'])
    plt.legend()
    plt.show()

if __name__=="__main__":
    from sys import stderr
    import CLI,sys
    my_opts = [
        # short, long, args, description
        ('p','psnr',0,'skips to PSNR calc'),
        ('t','type',1,'what algo to use'),
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
    mytype = 'fourier'
    myinfile = None
    myskip = False

    for o in opts:
        if o[0] == 'type':
            mytype = o[1]
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

