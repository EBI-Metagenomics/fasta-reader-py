import pytest
from fasta_reader import open_fasta, ParsingError


def test_fasta_correct():

    deflines = ["ID1", "ID2", "ID3", "ID4"]
    sequences = ["GAGUUA", "CAUAACAAATT", "AAGAA", "AAGAA"]

    f = open_fasta("fasta_reader/test/correct.seq")
    item = f.read_item()
    assert item.defline == deflines[0]
    assert item.sequence == sequences[0]

    item = f.read_item()
    assert item.defline == deflines[1]
    assert item.sequence == sequences[1]

    item = f.read_item()
    assert item.defline == deflines[2]
    assert item.sequence == sequences[2]

    item = f.read_item()
    assert item.defline == deflines[3]
    assert item.sequence == sequences[3]

    with pytest.raises(StopIteration):
        f.read_item()

    f.close()

    f = open_fasta("fasta_reader/test/correct.seq")
    for i, item in enumerate(f):
        assert item.defline == deflines[i]
        assert item.sequence == sequences[i]
    f.close()

    f = open_fasta("fasta_reader/test/correct.seq")
    items = f.read_items()
    for i in range(len(deflines)):
        assert items[i].defline == deflines[i]
        assert items[i].sequence == sequences[i]
    f.close()

    with open_fasta("fasta_reader/test/correct.seq") as f:
        for i, item in enumerate(f):
            assert item.defline == deflines[i]
            assert item.sequence == sequences[i]

    with open_fasta("fasta_reader/test/correct.seq") as f:
        f.close()


def test_fasta_damaged():

    with open_fasta("fasta_reader/test/damaged1.seq") as f:
        with pytest.raises(ParsingError):
            f.read_item()

    with open_fasta("fasta_reader/test/damaged2.seq") as f:
        with pytest.raises(ParsingError):
            f.read_item()

    with open_fasta("fasta_reader/test/damaged3.seq") as f:
        f.read_item()
        with pytest.raises(ParsingError):
            f.read_item()
