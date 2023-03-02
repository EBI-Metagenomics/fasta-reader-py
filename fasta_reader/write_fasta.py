import fsspec

from fasta_reader.anyfile import AnyFile
from fasta_reader.uri import URI
from fasta_reader.writer import Writer

__all__ = ["write_fasta"]


def write_fasta(uri: URI, ncols=60) -> Writer:
    """
    Open a FASTA file for writing.

    Parameters
    ----------
    uri
        Local or remote file address.

    Returns
    -------
    FASTA writer.
    """
    of = fsspec.open(uri, "wt", compression="infer")
    assert isinstance(of, fsspec.core.OpenFile)

    try:
        stream = of.open()
        isinstance(stream, fsspec.core.PickleableTextIOWrapper)
    except Exception:
        of.close()
        raise

    return Writer(AnyFile(of, stream), ncols)
