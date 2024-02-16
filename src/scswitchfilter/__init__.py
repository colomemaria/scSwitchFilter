from .bam2sam import bam2sam
from .sam2tsv import sam2tsv
from .generate_negative_matrix import generate_negative_matrix
from importlib.metadata import version, PackageNotFoundError


try:
    __version__ = version("scswfilt")
except PackageNotFoundError:
    # package is not installed
    pass
