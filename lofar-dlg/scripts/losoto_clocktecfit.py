#!/usr/bin/env python
#
#     LOFAR prefactor pipeline demonstrator
#     Copyright (C) 2018  ASTRON (Netherlands Institute for Radio Astronomy)
#     P.O.Box 2, 7990 AA Dwingeloo, The Netherlands
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import argparse
import subprocess as SP
from os import mkdir, chdir

parser = argparse.ArgumentParser(description="Wrapper around BBS calibration.")
parser.add_argument("-i", "--inh5", required=True, help="Input HDF5 file")
parser.add_argument("-d", "--outdir", required=True, help="Output directory")
parser.add_argument("-c", "--numcpus", required=True, help="Number of cpus to use")
parser.add_argument("-p", "--prefix",  required=True, help="Prefix to use")
args = parser.parse_args()

mkdir(args.outdir)

os.chdir(args.outdir)

command = ["fit_clocktec_initialguess_losoto.py", args.inh5, args.prefix, args.numcpus]

retval = SP.call(command)

if retval != 0:
    raise SP.CalledProcessError(retval, command)



