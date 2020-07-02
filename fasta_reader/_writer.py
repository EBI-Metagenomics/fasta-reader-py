import sys
import pathlib
from typing import IO, Union


class FASTAWriter:
    def __init__(
        self, file: Union[str, pathlib.Path, IO[str]], ncols: int = sys.maxsize
    ):
        if isinstance(file, str):
            file = pathlib.Path(file)

        if isinstance(file, pathlib.Path):
            file = open(file, "w")

        self._file = file
        self._ncols = ncols

    def write_item(self, defline: str, sequence: str):
        """
        Write item.
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
