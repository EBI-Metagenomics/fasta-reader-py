import io

from fsspec.core import OpenFile, PickleableTextIOWrapper

__all__ = ["AnyFile"]


class AnyFile(io.TextIOWrapper):
    def __init__(self, of: OpenFile, stream: PickleableTextIOWrapper):
        self._of = of
        self._stream = stream
        super().__init__(*stream.args)

    def close(self):
        super().close()
        self._of.close()
