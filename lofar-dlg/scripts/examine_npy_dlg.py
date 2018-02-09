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
from os import mkdir
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import pylab
from os.path import join as ojoin


parser = argparse.ArgumentParser(description="Wrapper around BBS calibration.")
parser.add_argument("-d", "--outdir", required=True, help="Output directory")
parser.add_argument("-a", "--ampl", required=True, help="Amplitude array location")
parser.add_argument("-c", "--ctdir", required=True, help="Clock/TEC solutions dir")
parser.add_argument("-p", "--prefix",  required=True, help="Prefix to use for Clock/TEC npy files")

args = parser.parse_args()

calsource =
mkdir(args.outdir)

amparray   = np.load(ojoin(args.ampl, '_amplitude_array.npy'))
clockarray = np.load(ojoin(args.ctdir, 'fitted_data_dclock_' + args.prefix + '_1st.sm.npy'))
dtecarray  = np.load(ojoin(args.ampl, 'fitted_data_dTEC_'   + args.prefix + '_1st.sm.npy'))

### From here just copy-paste from prefactor, adding the outdir

numants = len(dtecarray[0,:])

for i in range(0,numants):
    pylab.plot(dtecarray[:,i])
pylab.xlabel('Time')
pylab.ylabel('dTEC [$10^{16}$ m$^{-2}$]')
pylab.savefig(ojoin(args.outdir, 'dtec_allsols.png'))
pylab.close()
pylab.cla()

for i in range(0,numants):
    pylab.plot(1e9*clockarray[:,i])
pylab.xlabel('Time')
pylab.ylabel('dClock [ns]')
pylab.savefig(ojoin(args.outdir, 'dclock_allsols.png'))
pylab.close()
pylab.cla()


for i in range(0,numants):
  pylab.plot(np.median(amparray[i,:,:,0], axis=0))
  pylab.plot(np.median(amparray[i,:,:,1], axis=0))
pylab.xlabel('Subband number')
pylab.ylabel('Amplitude')
pylab.ylim(0,2.*np.median(amparray))
pylab.savefig(ojoin(args.outdir, 'amp_allsols.png'))
pylab.close()
pylab.cla()
