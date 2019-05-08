"""Class to store PHASER rotation scores"""

__author__ = "Adam Simpkin"
__date__ = "27 Dec 2017"
__version__ = "0.1"

from simbad.core import ScoreBase


class PhaserRotationScore(ScoreBase):
    """An phaser rotation scoring class"""

    __slots__ = ("pdb_code", "dat_path", "llg", "rfz")

    def __init__(self, pdb_code, dat_path, llg, rfz):
        self.pdb_code = pdb_code
        self.dat_path = dat_path
        self.llg = llg
        self.rfz = rfz

    def __repr__(self):
        string = "{name}(pdb_code={pdb_code} dat_path={dat_path} llg={llg} rfz={rfz})"
        return string.format(name=self.__class__.__name__, **{k: getattr(self, k) for k in self.__slots__})

    def _as_dict(self):
        """Convert the :obj:`PhaserRotationScore <simbad.core.phaser_score.PhaserRotationScore>`
        object to a dictionary"""
        return {k: getattr(self, k) for k in self.__slots__}


class PhaserTranslationScore(ScoreBase):
    """An phaser translation scoring class"""

    __slots__ = ("pdb_code", "dat_path", "rllg", "rfz", "tllg", "tfz")

    def __init__(self, pdb_code, dat_path, rllg, rfz, tllg, tfz):
        self.pdb_code = pdb_code
        self.dat_path = dat_path
        self.rllg = rllg
        self.rfz = rfz
        self.tllg = tllg
        self.tfz = tfz

    def __repr__(self):
        string = "{name}(pdb_code={pdb_code} dat_path={dat_path} rllg={rllg} rfz={rfz} tllg={tllg} tfz={tfz})"
        return string.format(name=self.__class__.__name__, **{k: getattr(self, k) for k in self.__slots__})

    def _as_dict(self):
        """Convert the :obj:`PhaserTranslationScore <simbad.core.phaser_score.PhaserTranslationScore>`
        object to a dictionary"""
        return {k: getattr(self, k) for k in self.__slots__}