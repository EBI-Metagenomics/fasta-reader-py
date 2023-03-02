from typing import TextIO

__all__ = ["Writer"]


class Writer:
    """
    FASTA writer.
    """

    def __init__(self, stream: TextIO, ncols: int = 60):
        """
        Parameters
        ----------
        file
            Writable stream of text.
        ncols
            Number of columns for formatting the output.
        """
        self._stream = stream
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
        self._stream.write(">" + defline + "\n")
        for i in range(0, len(sequence), self._ncols):
            seq = sequence[i : i + min(self._ncols, len(sequence) - i)]
            self._stream.write(seq + "\n")

    def close(self):
        self._stream.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
