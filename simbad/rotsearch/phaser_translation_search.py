#!/usr/bin/env ccp4-python
"""Module to run phaser translation search on a model

TODO: Update this module to use Phaser python interface"""

__author__ = "Adam Simpkin"
__date__ = "07 May 2019"
__version__ = "1.0"

import os
from pyjob import cexec
from pyjob.platform import EXE_EXT

class Phaser(object):
    """Class to run PHASER"""

    def __init__(self, hklin, f, i, logfile, pdbin, rlist, sigf, sigi, solvent, timeout, work_dir, eid):
        self._f = None
        self._hklin = None
        self._i = None
        self._logfile = None
        self._pdbin = None
        self._rlist = None
        self._sigf = None
        self._sigi = None
        self._solvent = None
        self._timeout = None
        self._work_dir = None

        self.eid = eid
        self.f = f
        self.hklin = hklin
        self.i = i
        self.logfile = logfile
        self.pdbin = pdbin
        self.rlist = rlist
        self.sigf = sigf
        self.sigi = sigi
        self.solvent = solvent
        self.timeout = timeout
        self.work_dir = work_dir

    @property
    def f(self):
        """The F label from the input hkl"""
        return self._f

    @f.setter
    def f(self, f):
        """Define the F label from the input hkl"""
        self._f = f

    @property
    def hklin(self):
        """The input hkl file"""
        return self._hklin

    @hklin.setter
    def hklin(self, hklin):
        """Define the input hkl file"""
        self._hklin = hklin

    @property
    def i(self):
        """The I label from the input hkl"""
        return self._i

    @i.setter
    def i(self, i):
        """Define the I label from the input hkl"""
        self._i = i

    @property
    def logfile(self):
        """The logfile output"""
        return self._logfile

    @logfile.setter
    def logfile(self, logfile):
        """Define the output logfile"""
        self._logfile = logfile

    @property
    def pdbin(self):
        """The input pdb file"""
        return self._pdbin

    @pdbin.setter
    def pdbin(self, pdbin):
        """Define the input pdb file"""
        self._pdbin = pdbin

    @property
    def rlist(self):
        """The list or orientations from the rotation function"""
        return self._rlist

    @rlist.setter
    def rlist(self, rlist):
        """The list or orientations from the rotation function"""
        self._rlist = rlist

    @property
    def sigf(self):
        """The SIGF label from the input hkl"""
        return self._sigf

    @sigf.setter
    def sigf(self, sigf):
        """Define the SIGF label from the input hkl"""
        self._sigf = sigf

    @property
    def sigi(self):
        """The SIGI label from the input hkl"""
        return self._sigi

    @sigi.setter
    def sigi(self, sigi):
        """Define the SIGI label from the input hkl"""
        self._sigi = sigi

    @property
    def solvent(self):
        """The estimated solvent content of the crystal"""
        return self._solvent

    @solvent.setter
    def solvent(self, solvent):
        """Define the estimated solvent content of the crystal"""
        self._solvent = solvent

    @property
    def timeout(self):
        """The time in minutes before phaser is killed"""
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """Define the time in minutes before phaser should be killed"""
        self._timeout = timeout

    def run(self):
        """Function to run the translation function using PHASER"""

        current_work_dir = os.getcwd()
        if os.path.exists(self.work_dir):
            os.chdir(self.work_dir)
        else:
            os.makedirs(self.work_dir)
            os.chdir(self.work_dir)

        cmd = [os.path.join(os.environ['CCP4'], 'bin', 'phaser' + EXE_EXT)]

        if self.i != 'None' and self.sigi != 'None':
            labin = "LABIN  I={0} SIGI={1}".format(self.i, self.sigi)
        elif self.f != 'None' and self.sigf != 'None':
            labin = "LABIN  F={0} SIGF={1}".format(self.f, self.sigf)
        else:
            msg = "No flags for intensities or amplitudes have been provided"
            raise RuntimeError(msg)

        key = """
        TITLE phaser_translation_search
        MODE MR_TRA
        ROOT "{0}"
        HKLIN "{1}"
        {2}
        SGALTERNATIVE SELECT NONE
        ENSEMBLE PDB &
            PDB "{3}" IDENT {4}
        COMPOSITION BY SOLVENT
        COMPOSITION PERCENTAGE {5}
        @ "{6}"
        """.format(self.work_dir, self.hklin, labin, self.pdbin, self.eid, self.solvent, self.rlist)

        stdout = cexec(cmd, stdin=key)
        print(stdout)
        with open(self.logfile, 'a') as f_out:
            f_out.write(stdout)

        os.chdir(current_work_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Runs rotation search using PHASER', prefix_chars="-")

    group = parser.add_argument_group()
    group.add_argument('-eid', type=str,
                       help="The estimated sequence identity")
    group.add_argument('-f', type=str,
                       help="The column label for F")
    group.add_argument('-hklin', type=str,
                       help="Path the input hkl file")
    group.add_argument('-i', type=str,
                       help="The column label for I")
    group.add_argument('-logfile', type=str,
                       help="Path to the ouput log file")
    group.add_argument('-pdbin', type=str,
                       help="Path to the input pdb file")
    group.add_argument('-rlist', type=str,
                       help="The list of orientations from the rotation function")
    group.add_argument('-sigf', type=str,
                       help="The column label for SIGF")
    group.add_argument('-sigi', type=str,
                       help="The column label for SIGI")
    group.add_argument('-solvent', type=float,
                       help="The estimated solvent content of the crystal")
    group.add_argument('-timeout', type=int, default=0,
                       help="The time in mins before phaser will kill a job")
    group.add_argument('-work_dir', type=str,
                       help="Path to the working directory")
    args = parser.parse_args()

    phaser = Phaser(**vars(args))
    phaser.run()
