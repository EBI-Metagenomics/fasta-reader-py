from fasta_reader.filepath import FilePath
from fasta_reader.reader import Reader

__all__ = ["read_fasta"]


def read_fasta(uri: FilePath) -> Reader:
    """
    Open a FASTA file for reading.

    Parameters
    ----------
    uri
        Local or remote file address.

    Returns
    -------
    FASTA reader.
    """
    return Reader(uri)
