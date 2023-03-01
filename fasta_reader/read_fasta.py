from io import TextIOWrapper

import fsspec

from fasta_reader.reader import Reader

__all__ = ["read_fasta"]


def read_fasta(uri: str) -> Reader:
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
    of = fsspec.open(uri, "rt", compression="infer")
    assert isinstance(of, fsspec.core.OpenFile)
    stream = of.open()
    isinstance(stream, TextIOWrapper)
    return Reader(stream)
