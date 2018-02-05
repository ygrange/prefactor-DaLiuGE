#!/usr/bin/env python

import argparse
import subprocess as SP

def check_checkmark(fil):
    print("CHECK {fil}".format(fil=fil))

parser = argparse.ArgumentParser()
parser.add_argument('inpfiles', metavar='INP', nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('-s', '--solset', help='Solution-set name (default=sol###)', type=str, default="sol000")
parser.add_argument('-c', '--complevel', type=int, default=5,
               help='Compression level from 0 (no compression, fast) to 9 (max compression, slow) (default=5)')
parser.add_argument('-o', '--output', help='Output h5 file name')
args = parser.parse_args()

cmd = ["/home/lofar-dlg/opt/prefactor/scripts/losotoImporter.py", args.output, "-c", str(args.complevel), "-s", args.solset]
cmd.extend(args.inpfiles)

retval = SP.call(cmd)

if retval != 0:
     raise SP.CalledProcessError(retval, command)
