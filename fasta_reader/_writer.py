from pathlib import Path
from typing import IO, Union

from xopen import xopen

__all__ = ["FASTAWriter", "write_fasta"]


class FASTAWriter:
    """
    FASTA writer.
    """

    def __init__(self, file: Union[str, Path, IO[str]], ncols: int = 60):
        """
        Parameters
        ----------
        file
            File path or IO stream.
        ncols
            Number of columns of sequence output.
        """
        if isinstance(file, str):
            file = Path(file)

        if isinstance(file, Path):
            file = xopen(file, "w")

        self._file = file
        self._ncols = ncols

    def write_item(self, defline: str, sequence: str):
        """
        Write item.

        Attributes
        ----------
        defline
            Description line.
        sequence
            Sequence.
        """
        self._file.write(">" + defline + "\n")
        for i in range(0, len(sequence), self._ncols):
            seq = sequence[i : i + min(self._ncols, len(sequence) - i)]
            self._file.write(seq + "\n")

    def close(self):
        """
        Close the associated stream.
        """
        self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del exception_type
        del exception_value
        del traceback
        self.close()


def write_fasta(file: Union[str, Path, IO[str]], ncols=60) -> FASTAWriter:
    """
    Open a FASTA file for writing.

    Parameters
    ----------
    file
        File path or IO stream.

    Returns
    -------
    FASTA writer.
    """
    return FASTAWriter(file, ncols)
