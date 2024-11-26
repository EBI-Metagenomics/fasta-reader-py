import textwrap

from fasta_reader.item import Item


__all__ = ["Formatter"]


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


class Formatter:
    def __init__(self, chunk_size=8, width=80):
        self._chunk_size = chunk_size
        self._width = width

    def format(self, x: Item):
        head = f">{x.defline}"
        rows = [i for i in chunks(x.sequence, self._chunk_size)]
        body = "\n".join(textwrap.wrap(" ".join(rows), width=self._width))
        return f"{head}\n{body}"
