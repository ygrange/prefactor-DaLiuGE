# DaLiuGE wrapper for the prefactor python scripts

import six
import find_skymodel_cal
from helpers import check_donemark

class find_skymodel_cal(BarrierAppDROP):
    def run(self):
        skymodel_path = "/home/dfms/opt/prefactor/skymodels"
        for inDrop in self.inputs:
            if inDrop.name == "MS copy":
                input_MS = inDrop.path
            if inDrop.name == "FlagAve Donemark":
                donemark = inDrop
            else:
                raise Exception("Unrecognised DROP provided {dn}. Bailing out.".format(dn=inDrop.name))

        if len(self.outputs) != 1:
            raise Exception("This application writes only one DROP")

        check_donemark(donemark)

        outDrop = self.outputs[0]

        found_skymodel = find_skymodel_cal.main(input_MS, skymodel_path)
        with open(found_skymodel) as skf:
            outdrop.write(six.b(str(skf.read())))
