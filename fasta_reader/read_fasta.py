import fsspec

from fasta_reader.anyfile import AnyFile
from fasta_reader.reader import Reader
from fasta_reader.uri import URI

__all__ = ["read_fasta"]


def read_fasta(uri: URI) -> Reader:
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

    try:
        stream = of.open()
        isinstance(stream, fsspec.core.PickleableTextIOWrapper)
    except Exception:
        of.close()
        raise

    return Reader(AnyFile(of, stream))
