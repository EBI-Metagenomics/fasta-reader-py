from __future__ import annotations

from dataclasses import dataclass

__all__ = ["Item"]


@dataclass
class Item:
    """
    FASTA item.

    Attributes
    ----------
    defline
        Description line.
    sequence
        Sequence.
    """

    defline: str
    sequence: str

    @property
    def id(self) -> str:
        """
        Identification.

        Returns
        -------
        Identification.
        """
        return self.defline.split(maxsplit=1)[0]

    @id.setter
    def id(self, val: str):
        if self.has_description:
            self.defline = val + " " + self.description
        else:
            self.defline = val

    @property
    def has_description(self) -> bool:
        """
        Does it has description?

        Returns
        -------
        ``True`` if it does contain description; ``False`` otherwise.
        """
        return len(self.defline.split()) > 1

    @property
    def description(self) -> str:
        """
        Description (if any).

        It will raise `RuntimeError` if it has no description.

        Returns
        -------
        Description.

        Raises
        ------
        RuntimeError
            If it has no description.
        """
        if not self.has_description:
            raise RuntimeError("It does not have a description.")
        tgt_id = self.id
        return self.defline[len(tgt_id) + 1 :]

    def __iter__(self):
        yield self.defline
        yield self.sequence

    def clone(self) -> Item:
        """
        Return a clone of itself.

        Returns
        -------
        FASTA item.
        """
        from copy import copy

        return copy(self)
