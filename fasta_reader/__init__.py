from ._cli import cli
from ._parser import FASTAItem, FASTAParser, ParsingError, open_fasta
from ._testit import test
from ._writer import FASTAWriter

__version__ = "0.0.4"

__all__ = [
    "FASTAItem",
    "FASTAParser",
    "FASTAWriter",
    "ParsingError",
    "__version__",
    "cli",
    "open_fasta",
    "test",
]
