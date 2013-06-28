def run_and_print(comm):
    from subprocess import check_call,check_output
    print 'running',' '.join(comm)
    check_output(comm)

def do_graphics(compressions):
    global myinfile
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

    commlist_fourier = map(lambda x: ['python2','3chan.py','-c',str(x[0]),'-o',x[1],myinfile],
                           zip(compressions,names_fourier))
    commlist_haar = map(lambda x: ['python2','wave_img.py','-w','db2','--smooth',
                                  '-c',x[0],'-o',x[1],myinfile],
                        zip(compressions,names_haar))
    commlist_db2 = map(lambda x: ['python2','wave_img.py','-w','haar','--smooth',
                                  '-c',x[0],'-o',x[1],myinfile],
                       zip(compressions,names_haar))
 
    map(run_and_print,commlist_fourier)
    map(run_and_print,commlist_haar)
    map(run_and_print,commlist_db2)

    

if __name__=="__main__":
    from sys import stderr
    import CLI,sys
    my_opts = [
        # short, long, args, description
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

    for o in opts:
        if o[0] == 'type':
            mytype = o[1]
        elif o[0] == 'infile':
            myinfile = o[1]
        elif o[0] == 'help':
            print my_usage
            exit(1)

    if len(args) == 1: # additional IOError
        print my_usage.short()
        exit(1)
  
    do_graphics(args[1:])

