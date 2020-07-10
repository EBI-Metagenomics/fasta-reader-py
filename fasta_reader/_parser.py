import pathlib
from dataclasses import dataclass
from typing import IO, Iterator, List, Union

from more_itertools import peekable


class ParsingError(Exception):
    pass


@dataclass
class FASTAItem:
    defline: str
    sequence: str

    @property
    def id(self) -> str:
        return self.defline.split()[0]

    @property
    def desc(self) -> str:
        tgt_id = self.id
        return self.defline[len(tgt_id) + 1 :]

    def __iter__(self):
        yield self.defline
        yield self.sequence


class FASTAParser:
    def __init__(self, file: Union[str, pathlib.Path, IO[str]]):
        if isinstance(file, str):
            file = pathlib.Path(file)

        if isinstance(file, pathlib.Path):
            file = open(file, "r")

        self._file = file
        self._lines = peekable(line for line in file)

    def read_item(self) -> FASTAItem:
        """
        Get the next item.
        """
        defline = self._next_defline()
        sequence = self._next_sequence()
        return FASTAItem(defline, sequence)

    def read_items(self) -> List[FASTAItem]:
        """
        Get the list of all items.
        """
        return list(self)

    def close(self):
        """
        Close the associated stream.
        """
        self._file.close()

    def _next_defline(self) -> str:
        while True:
            line = next(self._lines)
            if line == "":
                raise StopIteration

            line = line.strip()
            if line.startswith(">"):
                return line[1:]
            if line != "":
                raise ParsingError()

    def _next_sequence(self) -> str:
        lines = []
        while True:
            line = next(self._lines)
            if line == "":
                raise ParsingError()

            line = line.strip()
            if not line.startswith(">"):
                lines.append(line)
                if self._sequence_continues():
                    continue
                return "".join(lines)
            if line != "":
                raise ParsingError()

    def _sequence_continues(self):
        try:
            next_line = self._lines.peek()
        except StopIteration:
            return False

        if next_line == "":
            return False
        next_line = next_line.strip()
        return len(next_line) > 0 and not next_line.startswith(">")

    def __iter__(self) -> Iterator[FASTAItem]:
        while True:
            try:
                yield self.read_item()
            except StopIteration:
                return

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del exception_type
        del exception_value
        del traceback
        self.close()


def open_fasta(file: Union[str, pathlib.Path, IO[str]]) -> FASTAParser:
    """
    Open a FASTA file.

    Parameters
    ----------
    file : Union[str, pathlib.Path, IO[str]]
        File path or IO stream.

    Returns
    -------
    parser : FASTAParser
        FASTA parser.
    """
    return FASTAParser(file)
