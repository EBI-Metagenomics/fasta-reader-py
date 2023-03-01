from fasta_reader.writer import Writer
from fasta_reader.filepath import FilePath
from xopen import xopen

__all__ = ["write_fasta"]


def write_fasta(filename: FilePath, ncols=60) -> Writer:
    """
    Open a FASTA file for writing.

    Parameters
    ----------
    file
        File path.

    Returns
    -------
    FASTA writer.
    """
    return Writer(xopen(filename, "w"), ncols)
