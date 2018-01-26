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
from lofar_helpers import check_donemark 
from shutil import copytree

parser = argparse.ArgumentParser(description="Copy measurementset from local to shared space.")
parser.add_argument("-d", "--donemark", required=True, help="Donemark file")
parser.add_argument("-o", "--msout", required=True, help="output MS")
parser.add_argument("-i", "--msin", required=True, help="input MS")
args = parser.parse_args()

check_donemark(args.donemark)

copytree(args.msin, args.msout)


    
