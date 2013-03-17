#######################################################################
#
# Copyright (c) 2005 Guoqiang Duan. All Rights Reserved.
#
#######################################################################

"""
The command line script to run the generator.

$Id: run.py 11 2005-12-24 09:13:33Z duan $
"""

__version__='$Revision: 11 $'[11:-2]
__author__ = "Duan Guoqiang (mattgduan@gmail.com)"


import sys
import getopt

#import PyStartup

import Generator
import util


def usage(msg=''):
    print """USAGE: %s [-h] [-vq]

Options:
    -h/--help         -- print this message
    -v                -- verbose output
    -q                -- quiet, no output

"""%( sys.argv[0] )
    if msg:
        print >> sys.stderr, msg
    
    sys.exit(1)


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hvq', ['help'])
    except getopt.error, msg:
        usage(msg)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()

        if opt in ('-v'):
            util._mode = util.DEBUG_VERBOSE
        elif opt in ('-q'):
            util._mode = util.DEBUG_QUIET

    gen = Generator.Generator()
    gen.process()

