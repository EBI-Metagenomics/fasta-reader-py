from fasta_reader.reader import Reader
from fasta_reader.filepath import FilePath
from xopen import xopen

__all__ = ["read_fasta"]


def read_fasta(filename: FilePath) -> Reader:
    """
    Open a FASTA file for reading.

    Parameters
    ----------
    file
        File path.

    Returns
    -------
    FASTA reader.
    """
    return Reader(xopen(filename, "r"))
