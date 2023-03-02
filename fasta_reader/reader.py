from typing import Iterator, List, TextIO

from fasta_reader.errors import ParsingError
from fasta_reader.item import Item

__all__ = ["Reader"]


class Reader:
    """
    FASTA reader.
    """

    def __init__(self, stream: TextIO):
        """
        Parameters
        ----------
        file
            Readable stream of text.
        """
        self._stream = stream
        self._line_number = -1
        self._line: str = ""
        self._eof = False
        self._readline()

    def read_item(self) -> Item:
        """
        Get the next item.

        Returns
        -------
        Next item.
        """
        self._skip_blanklines()
        if self._eof:
            raise StopIteration

        return Item(self._next_defline(), self._next_sequence())

    def read_items(self) -> List[Item]:
        """
        Get the list of all items.

        Returns
        -------
        List of all items.
        """
        return list(self)

    def close(self):
        self._stream.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def _readline(self):
        line = self._stream.readline()
        self._eof = not line
        if self._eof:
            return
        self._line = line.strip()
        self._line_number += 1

    def _skip_blanklines(self):
        while not self._eof and self._line == "":
            self._readline()

    def _next_defline(self) -> str:
        if not self._line.startswith(">"):
            raise ParsingError(self._line_number)

        defline = self._line[1:]
        self._readline()
        return defline

    def _next_sequence(self) -> str:
        lines = []
        while not self._eof and self._line and not self._line.startswith(">"):
            lines.append(self._line)
            self._readline()

        return "".join(lines)

    def __iter__(self) -> Iterator[Item]:
        while True:
            try:
                yield self.read_item()
            except StopIteration:
                return
