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

from datetime import datetime

try:
    from __main__ import __file__ as functionname
except ImportError: # Running in a python shell
    functionname = 'shell_run.py'

def create_donemark(fname):
    file_content = "{functionname} done on {timestamp}\n"
    timestamp = datetime.now().isoformat()
    with open(fname, "w") as wrf:
        wrf.write(file_content.format(functionname=functionname,
                                      timestamp=timestamp))
def check_donemark(fname):
    with open(fname) as fh:
        print(fh.read())
