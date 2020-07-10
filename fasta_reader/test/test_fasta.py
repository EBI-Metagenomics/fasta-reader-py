import pytest

from fasta_reader import ParsingError, open_fasta


def _test_fasta_correct(filepath):
    deflines = ["ID1", "ID2", "ID3", "ID4"]
    sequences = ["GAGUUA", "CAUAACAAATT", "AAGAA", "AAGAA"]

    f = open_fasta(filepath)
    item = f.read_item()
    assert item.defline == deflines[0]
    assert item.id == deflines[0]
    assert item.desc == ""
    assert item.sequence == sequences[0]

    item = f.read_item()
    assert item.defline == deflines[1]
    assert item.id == deflines[1]
    assert item.desc == ""
    assert item.sequence == sequences[1]

    item = f.read_item()
    assert item.defline == deflines[2]
    assert item.id == deflines[2]
    assert item.desc == ""
    assert item.sequence == sequences[2]

    item = f.read_item()
    assert item.defline == deflines[3]
    assert item.id == deflines[3]
    assert item.desc == ""
    assert item.sequence == sequences[3]

    with pytest.raises(StopIteration):
        f.read_item()

    f.close()

    f = open_fasta(filepath)
    for i, item in enumerate(f):
        assert item.defline == deflines[i]
        assert item.sequence == sequences[i]
    f.close()

    f = open_fasta(filepath)
    items = f.read_items()
    for i, defline in enumerate(deflines):
        assert items[i].defline == defline
        assert items[i].sequence == sequences[i]
    f.close()

    with open_fasta(filepath) as f:
        for i, item in enumerate(f):
            assert item.defline == deflines[i]
            assert item.sequence == sequences[i]

    with open_fasta(filepath) as f:
        f.close()


def test_fasta_correct1(correct1):
    _test_fasta_correct(correct1)


def test_fasta_correct2(correct2):
    _test_fasta_correct(correct2)


def test_fasta_damaged(damaged1, damaged2, damaged3):

    with open_fasta(damaged1) as f:
        with pytest.raises(ParsingError):
            f.read_item()

    with open_fasta(damaged2) as f:
        with pytest.raises(ParsingError):
            f.read_item()

    with open_fasta(damaged3) as f:
        f.read_item()
        with pytest.raises(ParsingError):
            f.read_item()
