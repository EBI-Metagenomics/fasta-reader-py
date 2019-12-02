from ._reader import FASTAParser, Item, ParsingError, open_fasta
from ._testit import test

__version__ = "0.0.2"

__all__ = ["__version__", "test", "open_fasta", "FASTAParser", "ParsingError", "Item"]
