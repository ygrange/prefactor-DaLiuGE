#
#    LOFAR prefactor pipeline demonstrator
#    Copyright (C) 2018  ASTRON (Netherlands Institute for Radio Astronomy)
#    P.O.Box 2, 7990 AA Dwingeloo, The Netherlands#    All rights reserved
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston,
#    MA 02111-1307  USA
#
"""
Module container LOFAR prefactor helper functions
"""

import six
import os
import shutil
import find_skymodel_cal as find_skymodel_cal_wrapped

from dlg.drop import BarrierAppDROP

class CopyMS(BarrierAppDROP):
    '''
    This DROP copies a dataset to a input fileDROP.
    '''
    def run(self):
        if len(self.inputs) != 1:
            raise Exception("This application read only from one DROP")
        if len(self.outputs) != 1:
            raise Exception("This application writes only one DROP")

        inputDrop = self.inputs[0]
        desc = inputDrop.open()

        bufsize = 1
        buf = inputDrop.read(desc, bufsize)
        data = buf
        while buf:
            data += buf
            buf = inputDrop.read(desc, bufsize)

        shutil.copytree(data.decode(), str(self.outputs[0].path))


class DataSplitApp(BarrierAppDROP):
    '''
    This DROP splits the input data in subbands and returns a list thereof.
    '''
    def initialize(self, **kwargs):
        super(DataSplitApp, self).initialize(**kwargs)
        self.inpath = self._getArg(kwargs, 'inpath', None)

    def run(self):
        if len(self.inputs) != 0:
            raise Exception("This application does not read from DROPs")

        if not self.inpath:
            raise Exception("Infile needed for split")
        dirlist = [os.path.join(self.inpath, pth) for pth in
                   os.listdir(self.inpath) if
                   os.path.isdir(os.path.join(self.inpath, pth))]

        for counter, outputDROP in enumerate(self.outputs):
            outputDROP.write(str(six.b(dirlist[counter])))

class ParsetParseApp(BarrierAppDROP):
    '''
    This DROP parses a LOFAR Parset and addes the keys provided as input, writing it out to the OutputDROP
    '''

    def initialize(self, **kwargs):
        super(ParsetParseApp, self).initialize(**kwargs)
        self.step = self._getArg(kwargs, 'step', None)
        self.parsestr = kwargs
        if not self.step:
            raise Exception("Can't parse parset without step name")


    def run(self):
        mypath = os.path.dirname(__file__)
        pstemplate = os.path.join(mypath, "lofar_parsets", "{step}.parset".format(step=self.step))
        with open(pstemplate) as pst:
            pstext = pst.read()

        psparsed = pstext.format(**self.parsestr)

        for ip in self.inputs:
            uidint = str(ip.oid).split("_")[-2]
            psparsed = psparsed.replace("%i[{uid}]".format(uid=uidint),
                                        ip.path)
        for op in self.outputs:
            uidint = str(op.oid).split("_")[-2]
            psparsed = psparsed.replace("%o[{uid}]".format(uid=uidint),
                                        op.path)


        outputDrop = self.outputs[0]


        # Rely on whatever implementation we decide to use
        # for storing our data
        outputDrop.write(six.b(str(psparsed)))

class find_skymodel_cal(BarrierAppDROP):
    """wrapper around the tool to find skymodel and put it in a memoryDROP."""

    def run(self):
        if len(self.inputs) != 1:
             raise Exception("This application writes only one DROP")
        if len(self.outputs) != 1:
             raise Exception("This application writes only one DROP")

        skymodel_path = "/home/lofar-dlg/opt/prefactor/skymodels"
        input_MS = self.inputs[0].path

        outDrop = self.outputs[0]

        found_skymodel = find_skymodel_cal_wrapped.main(input_MS, skymodel_path)['SkymodelCal']

        with open(found_skymodel) as skf:
            outDrop.write(six.b(str(skf.read())))
