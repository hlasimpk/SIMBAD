"""Returns values for the top translation peak from a transearch log file"""

__author__ = "Adam Simpkin"
__date__ = "07 May 2019"
__version__ = "0.1"

import simbad.parsers


class PhaserTransearchParser(simbad.parsers._Parser):
    """Class to mine information from a phaser transearch logfile"""

    def __init__(self, logfile):
        super(PhaserTransearchParser, self).__init__(logfile)
        self.rfact = None
        self.rllg = None
        self.rfz = None
        self.tllg = None
        self.tfz = None
        self._parse()

    def _parse(self):
        """Parse information from the logfile"""
        with open(self.logfile, "r") as f_in:
            line = f_in.readline()
            while line:
                if "Minimum R-factor" in line:
                    fields = line.strip().split()
                    self.rfact = float(fields[-1])
                if "#SET" in line:
                    line = f_in.readline()
                    fields = line.strip().split()
                    self.rllg = float(fields[1])
                    self.rfz = float(fields[2])
                if "SET ROT*deep" in line:
                    line = f_in.readline()
                    fields = line.strip().split()
                    self.tllg = float(fields[2])
                    self.tfz = float(fields[3])
                line = f_in.readline()