import os
import typing

__all__ = ["FilePath"]

FilePath = typing.Union[str, os.PathLike]
