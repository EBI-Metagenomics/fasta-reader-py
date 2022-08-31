"""FASTA file reader/writer."""
from ._cli import cli
from ._reader import FASTAItem, FASTAReader, ParsingError, read_fasta
from ._writer import FASTAWriter, write_fasta

__version__ = "1.0.3"

__all__ = [
    "FASTAItem",
    "FASTAReader",
    "FASTAWriter",
    "ParsingError",
    "__version__",
    "cli",
    "read_fasta",
    "write_fasta",
]
