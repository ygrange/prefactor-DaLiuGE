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
from lofar_helpers import create_donemark 
from shutil import copytree

parser = argparse.ArgumentParser(description="Wrapper around BBS calibration.")
parser.add_argument("-i", "--inms", required=True, help="Output donemark file")
parser.add_argument("-d", "--donemark", required=True, help="Output donemark file")
parser.add_argument("-p", "--parset", required=True, help="parset file for NDPPP")
parser.add_argument("-s", "--skymodel", required=True, help="Skymodel file")
args = parser.parse_args()

command = ["calibrate-stand-alone", args.inms, args.parset, args.skymodel]

retval = SP.call(command)

if retval != 0:
    raise SP.CalledProcessError(retval, command)

create_donemark(args.donemark) 
