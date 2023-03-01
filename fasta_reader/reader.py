from typing import Iterator, List, TextIO

from more_itertools import peekable

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
        self._lines = peekable(line for line in self._stream)
        self._line_number = 0

    def read_item(self) -> Item:
        """
        Get the next item.

        Returns
        -------
        Next item.
        """
        defline = self._next_defline()
        sequence = self._next_sequence()
        return Item(defline, sequence)

    def read_items(self) -> List[Item]:
        """
        Get the list of all items.

        Returns
        -------
        List of all items.
        """
        return list(self)

    def close(self):
        """
        Close the associated stream.
        """
        self._stream.close()

    def _next_defline(self) -> str:
        while True:
            line = next(self._lines)
            self._line_number += 1
            if line == "":
                raise StopIteration

            line = line.strip()
            if line.startswith(">"):
                return line[1:]
            if line != "":
                raise ParsingError(self._line_number)

    def _next_sequence(self) -> str:
        lines = []
        while True:
            line = next(self._lines)
            self._line_number += 1
            if line == "":
                raise ParsingError(self._line_number)

            line = line.strip()
            if not line.startswith(">"):
                lines.append(line)
                if self._sequence_continues():
                    continue
                return "".join(lines)
            if line != "":
                raise ParsingError(self._line_number)

    def _sequence_continues(self):
        try:
            next_line = self._lines.peek()
        except StopIteration:
            return False

        if next_line == "":
            return False
        next_line = next_line.strip()
        return len(next_line) > 0 and not next_line.startswith(">")

    def __iter__(self) -> Iterator[Item]:
        while True:
            try:
                yield self.read_item()
            except StopIteration:
                return

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
