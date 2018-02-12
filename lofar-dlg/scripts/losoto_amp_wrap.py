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
from os import mkdir
from os.path import join as ojoin
from lofar_helpers import check_donemark, create_donemark

parser = argparse.ArgumentParser(description="Wrapper around BBS calibration.")
parser.add_argument("-i", "--inh5", required=True, help="Input HDF5 file")
parser.add_argument("-o", "--outdir", required=True, help="Output directory")
parser.add_argument("-c", "--chans", required=True, help="Chanels per sub band")
parser.add_argument("-d", "--donemark_in", required=True, help="Input donemark")
parser.add_argument("-e", "--donemark_out", required=True, help="Output donemark")
args = parser.parse_args()

check_donemark(args.donemark_in)
mkdir(args.outdir)


command = ["amplitudes_losoto_3.py", args.inh5, ojoin(args.outdir,""), args.chans]

retval = SP.call(command)

if retval != 0:
    raise SP.CalledProcessError(retval, command)

create_donemark(args.donemark_out)

