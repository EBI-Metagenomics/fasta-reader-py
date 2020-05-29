import pathlib
from typing import IO, Union


class FASTAWriter:
    def __init__(self, file: Union[str, pathlib.Path, IO[str]]):
        if isinstance(file, str):
            file = pathlib.Path(file)

        if isinstance(file, pathlib.Path):
            file = open(file, "w")

        self._file = file

    def write_item(self, defline: str, sequence: str):
        """
        Write item.
        """
        self._file.write(">" + defline + "\n")
        self._file.write(sequence + "\n")

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
